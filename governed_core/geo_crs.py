"""Deterministic, offline CRS resolution and coordinate transformation."""

import math
import os
import hashlib
from pathlib import Path
from dataclasses import dataclass

os.environ["PROJ_NETWORK"] = "OFF"

import pyproj
from pyproj import CRS, Transformer, datadir, database
from pyproj.exceptions import ProjError
from pyproj.network import is_network_enabled, set_network_enabled

from .geo_models import SourceAxisOrder


set_network_enabled(False)

EXPECTED_PYPROJ_VERSION = "3.7.2"
EXPECTED_PROJ_VERSION = "9.5.1"
EXPECTED_EPSG_VERSION = "v11.022"
EXPECTED_PROJ_DB_SHA256 = "47A7205D83BA6B7774B763F276AB57331F4DADE2B2CFBCC0D486677E6543350B"
EXPECTED_WHEEL_SHA256 = "11614A054CD86A2ED968A657D00987A86EEB91FDCBD9AD3310478685DC14A128"


def _packaged_proj_data_dir():
    package_dir = Path(pyproj.__file__).resolve().parent
    candidate = package_dir / "proj_dir" / "share" / "proj"
    return candidate if candidate.is_dir() else None


def _manifest_values_match():
    manifest = Path(__file__).resolve().parents[1] / "docs" / "governance" / "GEO_PROJ_REPRODUCIBILITY_MANIFEST.md"
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    required = (
        f"pyproj | `3.7.2`", f"PROJ runtime | `9.5.1`",
        f"EPSG `v11.022`", f"`proj.db` SHA-256 | `{EXPECTED_PROJ_DB_SHA256}`",
        f"wheel SHA-256 | `{EXPECTED_WHEEL_SHA256}`", "PROJ_NETWORK=OFF",
    )
    return all(value in text for value in required)


def verify_runtime_manifest():
    """Return a deterministic reason code when the pinned local runtime is invalid."""
    set_network_enabled(False)
    if is_network_enabled():
        return "GEO_NETWORK_ENABLED"
    if not _manifest_values_match():
        return "GEO_MANIFEST_MISMATCH"
    if pyproj.__version__ != EXPECTED_PYPROJ_VERSION:
        return "GEO_PROVIDER_VERSION_MISMATCH"
    if pyproj.proj_version_str != EXPECTED_PROJ_VERSION:
        return "GEO_PROJ_VERSION_MISMATCH"
    packaged = _packaged_proj_data_dir()
    if packaged is None:
        return "GEO_PROJ_DATA_UNAVAILABLE"
    os.environ["PROJ_DATA"] = str(packaged)
    datadir.set_data_dir(str(packaged))
    actual_dir = Path(datadir.get_data_dir()).resolve()
    if actual_dir != packaged.resolve():
        return "GEO_PROJ_DATA_FALLBACK"
    proj_db = actual_dir / "proj.db"
    if not proj_db.is_file():
        return "GEO_PROJ_DATABASE_UNAVAILABLE"
    digest = hashlib.sha256(proj_db.read_bytes()).hexdigest().upper()
    if digest != EXPECTED_PROJ_DB_SHA256:
        return "GEO_PROJ_DATABASE_HASH_MISMATCH"
    if database.get_database_metadata("EPSG.VERSION") != EXPECTED_EPSG_VERSION:
        return "GEO_EPSG_DATABASE_VERSION_MISMATCH"
    return None


@dataclass(frozen=True)
class CRSResolution:
    state: str
    identifier: str
    canonical_identifier: str | None = None
    reason_code: str | None = None


@dataclass(frozen=True)
class CoordinateTransformation:
    state: str
    latitude: float | None = None
    longitude: float | None = None
    operation: str | None = None
    reason_code: str | None = None


class CRSResolver:
    def __init__(self, target_identifier="EPSG:4326"):
        self.target_identifier = target_identifier

    def resolve(self, identifier):
        manifest_failure = verify_runtime_manifest()
        if manifest_failure:
            return CRSResolution("CRS_UNRESOLVED", identifier or "", reason_code=manifest_failure)
        if not isinstance(identifier, str) or not identifier.strip():
            return CRSResolution("CRS_UNRESOLVED", identifier or "", reason_code="CRS_UNRESOLVED")
        try:
            crs = CRS.from_user_input(identifier)
            if len(crs.axis_info) < 2:
                return CRSResolution("CRS_AXIS_ORDER_UNRESOLVED", identifier, reason_code="CRS_AXIS_ORDER_UNRESOLVED")
            canonical = crs.to_string() or identifier
            return CRSResolution("RESOLVED_CRS", identifier, canonical)
        except (ProjError, ValueError, TypeError):
            return CRSResolution("CRS_UNRESOLVED", identifier, reason_code="CRS_UNRESOLVED")


class CoordinateTransformer:
    def __init__(self, target_identifier="EPSG:4326"):
        self.target_identifier = target_identifier
        self.resolver = CRSResolver(target_identifier)

    def transform(self, source_crs, source_pair, source_axis_order):
        manifest_failure = verify_runtime_manifest()
        if manifest_failure:
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code=manifest_failure)
        source = self.resolver.resolve(source_crs)
        target = self.resolver.resolve(self.target_identifier)
        if source.state != "RESOLVED_CRS":
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code=source.reason_code)
        if target.state != "RESOLVED_CRS":
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code=target.reason_code)
        target_crs = CRS.from_user_input(self.target_identifier)
        if not target_crs.is_geographic or len(target_crs.axis_info) != 2:
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code="CRS_NOT_GEOGRAPHIC_LATLON")
        if source_axis_order == SourceAxisOrder.UNKNOWN.value:
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code="CRS_AXIS_ORDER_UNRESOLVED")
        try:
            first, second = (float(value) for value in source_pair)
            if not all(math.isfinite(value) for value in (first, second)):
                raise ValueError
            if source_axis_order == SourceAxisOrder.LONGITUDE_LATITUDE.value:
                x, y = first, second
            elif source_axis_order == SourceAxisOrder.LATITUDE_LONGITUDE.value:
                x, y = second, first
            else:
                axes = CRS.from_user_input(source_crs).axis_info
                first_direction = axes[0].direction.lower()
                x, y = ((second, first) if first_direction in {"north", "south"} else (first, second))
            transformer = Transformer.from_crs(
                source_crs, self.target_identifier, always_xy=True,
                only_best=True, allow_ballpark=False,
            )
            longitude, latitude = transformer.transform(x, y, errcheck=True)
            if not all(math.isfinite(value) for value in (latitude, longitude)):
                raise ValueError
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ValueError
            return CoordinateTransformation(
                "TRANSFORMED_COORDINATE", latitude, longitude,
                transformer.description or transformer.name,
            )
        except (ProjError, ValueError, TypeError, OverflowError):
            return CoordinateTransformation("TRANSFORMATION_UNAVAILABLE", reason_code="TRANSFORMATION_UNAVAILABLE")
