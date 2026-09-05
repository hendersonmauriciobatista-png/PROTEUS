-- MCM-WQ normalized, context-owned GEO reference and immutable provenance.
-- Legacy point_context_revision.geo_reference remains opaque and unchanged.

-- Persisted-database preflight.  These checks deliberately fail before any
-- GEO object is created; the migration runner supplies the outer transaction.
CREATE TEMP TABLE m020_preflight (check_id TEXT PRIMARY KEY);
CREATE TEMP TRIGGER m020_preflight_guard
BEFORE INSERT ON m020_preflight
WHEN (NEW.check_id = 'migration_019' AND NOT EXISTS (
          SELECT 1 FROM schema_migration
          WHERE migration_id = '019_mcm_wq_evaluation_authority_snapshot.sql'
            AND checksum = '8db22fa64588a01aef54978066fbd459794dd8710317ec4b99882a52608ffd36'
      ))
  OR (NEW.check_id = 'point_context_revision' AND NOT EXISTS (
          SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'point_context_revision'
      ))
  OR (NEW.check_id = 'schema_migration' AND NOT EXISTS (
          SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_migration'
      ))
  OR (NEW.check_id = 'context_id' AND NOT EXISTS (
          SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'context_revision_id'
      ))
  OR (NEW.check_id = 'required_context_columns' AND (
          NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'point_id')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'revision')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'purpose')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'water_context')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'point_type')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'geo_reference')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'created_at')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'effective_from')
          OR NOT EXISTS (SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'effective_until')
      ))
  OR (NEW.check_id = 'legacy_geo' AND NOT EXISTS (
          SELECT 1 FROM pragma_table_info('point_context_revision') WHERE name = 'geo_reference'
      ))
  OR (NEW.check_id = 'legacy_readable' AND EXISTS (
          SELECT 1 FROM point_context_revision
          WHERE context_revision_id IS NULL
      ))
  OR (NEW.check_id IN ('geo_reference', 'location_provenance') AND EXISTS (
          SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = NEW.check_id
      ))
  OR (NEW.check_id = 'reserved_objects' AND EXISTS (
          SELECT 1 FROM sqlite_master
          WHERE (type = 'index' AND name IN (
              'geo_reference_context_unique', 'geo_reference_state_lookup',
              'geo_reference_provenance_lookup', 'location_provenance_source_lookup'
          )) OR (type = 'trigger' AND name IN (
              'context_geo_link_required',
              'context_geo_link_immutable', 'geo_context_link_guard',
              'location_provenance_immutable_update', 'location_provenance_immutable_delete',
              'geo_reference_immutable_update', 'geo_reference_immutable_delete'
          ))
      ))
  OR (NEW.check_id = 'context_ids_unique' AND EXISTS (
          SELECT context_revision_id FROM point_context_revision
          GROUP BY context_revision_id HAVING COUNT(*) > 1
      ))
BEGIN SELECT RAISE(ABORT, 'Migration 020 preflight failed'); END;

INSERT INTO m020_preflight VALUES ('migration_019');
INSERT INTO m020_preflight VALUES ('schema_migration');
INSERT INTO m020_preflight VALUES ('point_context_revision');
INSERT INTO m020_preflight VALUES ('context_id');
INSERT INTO m020_preflight VALUES ('required_context_columns');
INSERT INTO m020_preflight VALUES ('legacy_geo');
INSERT INTO m020_preflight VALUES ('legacy_readable');
INSERT INTO m020_preflight VALUES ('geo_reference');
INSERT INTO m020_preflight VALUES ('location_provenance');
INSERT INTO m020_preflight VALUES ('reserved_objects');
INSERT INTO m020_preflight VALUES ('context_ids_unique');
DROP TRIGGER m020_preflight_guard;
DROP TABLE m020_preflight;

CREATE TEMP TABLE m020_legacy_snapshot AS
SELECT context_revision_id, geo_reference FROM point_context_revision;

CREATE TABLE location_provenance (
    provenance_id TEXT PRIMARY KEY CHECK (length(trim(provenance_id)) > 0),
    source_reference TEXT NOT NULL CHECK (length(trim(source_reference)) > 0),
    source_coordinate_1_raw TEXT NOT NULL CHECK (length(trim(source_coordinate_1_raw)) > 0),
    source_coordinate_2_raw TEXT NOT NULL CHECK (length(trim(source_coordinate_2_raw)) > 0),
    source_coordinate_1_numeric REAL,
    source_coordinate_2_numeric REAL,
    source_axis_order TEXT NOT NULL CHECK (source_axis_order IN (
        'LATITUDE_LONGITUDE', 'LONGITUDE_LATITUDE', 'SOURCE_DECLARED_AXES', 'UNKNOWN'
    )),
    source_crs_identifier TEXT NOT NULL CHECK (length(trim(source_crs_identifier)) > 0),
    acquisition_method TEXT CHECK (acquisition_method IS NULL OR length(trim(acquisition_method)) > 0),
    captured_at TEXT,
    captured_at_status TEXT NOT NULL CHECK (captured_at_status IN ('KNOWN', 'UNKNOWN')),
    transformation_method TEXT,
    transformation_parameters TEXT,
    transformation_provenance TEXT,
    accuracy_or_uncertainty_kind TEXT CHECK (
        accuracy_or_uncertainty_kind IS NULL OR accuracy_or_uncertainty_kind IN ('ACCURACY', 'UNCERTAINTY')
    ),
    accuracy_or_uncertainty_value REAL,
    accuracy_or_uncertainty_unit TEXT,
    registered_at TEXT NOT NULL CHECK (length(trim(registered_at)) > 0),
    CHECK ((captured_at_status = 'KNOWN' AND captured_at IS NOT NULL)
        OR (captured_at_status = 'UNKNOWN' AND captured_at IS NULL)),
    CHECK ((transformation_method IS NULL AND transformation_provenance IS NULL)
        OR (transformation_method IS NOT NULL AND transformation_provenance IS NOT NULL
            AND length(trim(transformation_method)) > 0 AND length(trim(transformation_provenance)) > 0)),
    CHECK ((accuracy_or_uncertainty_kind IS NULL
            AND accuracy_or_uncertainty_value IS NULL AND accuracy_or_uncertainty_unit IS NULL)
        OR (accuracy_or_uncertainty_kind IS NOT NULL
            AND accuracy_or_uncertainty_value IS NOT NULL
            AND accuracy_or_uncertainty_unit IS NOT NULL
            AND length(trim(accuracy_or_uncertainty_unit)) > 0)),
    CHECK (accuracy_or_uncertainty_value IS NULL OR (
        typeof(accuracy_or_uncertainty_value) IN ('integer', 'real')
        AND accuracy_or_uncertainty_value = accuracy_or_uncertainty_value
        AND abs(accuracy_or_uncertainty_value) < 1.7976931348623157e308
        AND accuracy_or_uncertainty_value >= 0
    )),
    CHECK (source_coordinate_1_numeric IS NULL OR (
        typeof(source_coordinate_1_numeric) IN ('integer', 'real')
        AND source_coordinate_1_numeric = source_coordinate_1_numeric
        AND abs(source_coordinate_1_numeric) < 1.7976931348623157e308
    )),
    CHECK (source_coordinate_2_numeric IS NULL OR (
        typeof(source_coordinate_2_numeric) IN ('integer', 'real')
        AND source_coordinate_2_numeric = source_coordinate_2_numeric
        AND abs(source_coordinate_2_numeric) < 1.7976931348623157e308
    )),
    CHECK (
        ((length(registered_at) = 20 AND registered_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')
        OR (length(registered_at) = 27 AND registered_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z'))
    AND CAST(substr(registered_at, 6, 2) AS INTEGER) BETWEEN 1 AND 12
    AND CAST(substr(registered_at, 9, 2) AS INTEGER) BETWEEN 1 AND
        (CASE CAST(substr(registered_at, 6, 2) AS INTEGER)
            WHEN 2 THEN CASE WHEN (CAST(substr(registered_at, 1, 4) AS INTEGER) % 4 = 0
                AND (CAST(substr(registered_at, 1, 4) AS INTEGER) % 100 <> 0
                OR CAST(substr(registered_at, 1, 4) AS INTEGER) % 400 = 0)) THEN 29 ELSE 28 END
            WHEN 4 THEN 30 WHEN 6 THEN 30 WHEN 9 THEN 30 WHEN 11 THEN 30 ELSE 31
        END)
    AND CAST(substr(registered_at, 12, 2) AS INTEGER) BETWEEN 0 AND 23
    AND CAST(substr(registered_at, 15, 2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(registered_at, 18, 2) AS INTEGER) BETWEEN 0 AND 59),
    CHECK (captured_at IS NULL OR (
        (length(captured_at) = 20 AND captured_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')
        OR (length(captured_at) = 27 AND captured_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z')
    ) AND CAST(substr(captured_at, 6, 2) AS INTEGER) BETWEEN 1 AND 12
    AND CAST(substr(captured_at, 9, 2) AS INTEGER) BETWEEN 1 AND
        (CASE CAST(substr(captured_at, 6, 2) AS INTEGER)
            WHEN 2 THEN CASE WHEN (CAST(substr(captured_at, 1, 4) AS INTEGER) % 4 = 0
                AND (CAST(substr(captured_at, 1, 4) AS INTEGER) % 100 <> 0
                OR CAST(substr(captured_at, 1, 4) AS INTEGER) % 400 = 0)) THEN 29 ELSE 28 END
            WHEN 4 THEN 30 WHEN 6 THEN 30 WHEN 9 THEN 30 WHEN 11 THEN 30 ELSE 31
        END)
    AND CAST(substr(captured_at, 12, 2) AS INTEGER) BETWEEN 0 AND 23
    AND CAST(substr(captured_at, 15, 2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(captured_at, 18, 2) AS INTEGER) BETWEEN 0 AND 59)
);

CREATE TABLE geo_reference (
    geo_reference_id TEXT PRIMARY KEY CHECK (length(trim(geo_reference_id)) > 0),
    context_revision_id TEXT NOT NULL UNIQUE
        REFERENCES point_context_revision(context_revision_id)
        DEFERRABLE INITIALLY DEFERRED,
    availability_state TEXT NOT NULL CHECK (
        availability_state IN ('AVAILABLE', 'UNAVAILABLE', 'UNVERIFIED', 'LEGACY_UNCLASSIFIED')
    ),
    latitude REAL,
    longitude REAL,
    crs_identifier TEXT,
    location_provenance_id TEXT REFERENCES location_provenance(provenance_id),
    state_reason TEXT,
    registered_at TEXT NOT NULL CHECK (length(trim(registered_at)) > 0),
    CHECK (latitude IS NULL OR (
        typeof(latitude) IN ('integer', 'real') AND latitude = latitude
        AND abs(latitude) < 1.7976931348623157e308 AND latitude BETWEEN -90 AND 90
    )),
    CHECK (longitude IS NULL OR (
        typeof(longitude) IN ('integer', 'real') AND longitude = longitude
        AND abs(longitude) < 1.7976931348623157e308 AND longitude BETWEEN -180 AND 180
    )),
    CHECK (
        ((length(registered_at) = 20 AND registered_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')
        OR (length(registered_at) = 27 AND registered_at GLOB
            '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z'))
    AND CAST(substr(registered_at, 6, 2) AS INTEGER) BETWEEN 1 AND 12
    AND CAST(substr(registered_at, 9, 2) AS INTEGER) BETWEEN 1 AND
        (CASE CAST(substr(registered_at, 6, 2) AS INTEGER)
            WHEN 2 THEN CASE WHEN (CAST(substr(registered_at, 1, 4) AS INTEGER) % 4 = 0
                AND (CAST(substr(registered_at, 1, 4) AS INTEGER) % 100 <> 0
                OR CAST(substr(registered_at, 1, 4) AS INTEGER) % 400 = 0)) THEN 29 ELSE 28 END
            WHEN 4 THEN 30 WHEN 6 THEN 30 WHEN 9 THEN 30 WHEN 11 THEN 30 ELSE 31
        END)
    AND CAST(substr(registered_at, 12, 2) AS INTEGER) BETWEEN 0 AND 23
    AND CAST(substr(registered_at, 15, 2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(registered_at, 18, 2) AS INTEGER) BETWEEN 0 AND 59),
    CHECK (
        (availability_state = 'AVAILABLE'
            AND latitude IS NOT NULL AND longitude IS NOT NULL
            AND crs_identifier IS NOT NULL AND length(trim(crs_identifier)) > 0
            AND location_provenance_id IS NOT NULL AND state_reason IS NULL)
        OR (availability_state IN ('UNAVAILABLE', 'LEGACY_UNCLASSIFIED')
            AND latitude IS NULL AND longitude IS NULL AND crs_identifier IS NULL
            AND location_provenance_id IS NULL
            AND state_reason IS NOT NULL AND length(trim(state_reason)) > 0)
        OR (availability_state = 'UNVERIFIED'
            AND latitude IS NULL AND longitude IS NULL AND crs_identifier IS NULL
            AND location_provenance_id IS NOT NULL
            AND state_reason IS NOT NULL AND length(trim(state_reason)) > 0)
    )
);

ALTER TABLE point_context_revision ADD COLUMN geo_reference_id TEXT
    REFERENCES geo_reference(geo_reference_id) DEFERRABLE INITIALLY DEFERRED;

DROP TRIGGER context_revision_authorized_close;

INSERT INTO geo_reference(
    geo_reference_id, context_revision_id, availability_state,
    latitude, longitude, crs_identifier, location_provenance_id,
    state_reason, registered_at
)
SELECT 'legacy-geo-' || context_revision_id, context_revision_id,
       'LEGACY_UNCLASSIFIED', NULL, NULL, NULL, NULL,
       'LEGACY_OPAQUE_VALUE_NOT_SEMANTICALLY_PROVEN',
       replace(created_at, '+00:00', 'Z')
FROM point_context_revision;

UPDATE point_context_revision
SET geo_reference_id = 'legacy-geo-' || context_revision_id;

CREATE UNIQUE INDEX geo_reference_context_unique
    ON geo_reference(context_revision_id);
CREATE INDEX geo_reference_state_lookup ON geo_reference(availability_state);
CREATE INDEX geo_reference_provenance_lookup ON geo_reference(location_provenance_id);
CREATE INDEX location_provenance_source_lookup ON location_provenance(source_reference);

CREATE TRIGGER context_revision_authorized_close
BEFORE UPDATE ON point_context_revision
WHEN NOT (
    OLD.effective_until IS NULL AND NEW.effective_until IS NOT NULL
    AND NEW.effective_from IS OLD.effective_from
    AND NEW.context_revision_id IS OLD.context_revision_id
    AND NEW.point_id IS OLD.point_id
    AND NEW.revision IS OLD.revision
    AND NEW.purpose IS OLD.purpose
    AND NEW.water_context IS OLD.water_context
    AND NEW.point_type IS OLD.point_type
    AND NEW.geo_reference IS OLD.geo_reference
    AND NEW.created_at IS OLD.created_at
    AND NEW.geo_reference_id IS OLD.geo_reference_id
)
BEGIN SELECT RAISE(ABORT, 'point_context_revision immutable outside authorized close'); END;

CREATE TRIGGER context_geo_link_required
BEFORE INSERT ON point_context_revision
WHEN NEW.geo_reference_id IS NULL
  OR NOT EXISTS (SELECT 1 FROM geo_reference WHERE geo_reference_id = NEW.geo_reference_id)
BEGIN SELECT RAISE(ABORT, 'point context requires matching GEO reference'); END;

CREATE TRIGGER context_geo_link_immutable
BEFORE UPDATE OF geo_reference_id ON point_context_revision
WHEN NEW.geo_reference_id IS NOT OLD.geo_reference_id
BEGIN SELECT RAISE(ABORT, 'point context GEO link is immutable'); END;

CREATE TRIGGER geo_context_link_guard
BEFORE INSERT ON geo_reference
WHEN EXISTS (
    SELECT 1 FROM point_context_revision
    WHERE context_revision_id = NEW.context_revision_id
      AND geo_reference_id IS NOT NULL
      AND geo_reference_id IS NOT NEW.geo_reference_id
)
BEGIN SELECT RAISE(ABORT, 'GEO reference context link mismatch'); END;

CREATE TRIGGER location_provenance_immutable_update
BEFORE UPDATE ON location_provenance
BEGIN SELECT RAISE(ABORT, 'location provenance is immutable'); END;
CREATE TRIGGER location_provenance_immutable_delete
BEFORE DELETE ON location_provenance
BEGIN SELECT RAISE(ABORT, 'location provenance is immutable'); END;
CREATE TRIGGER geo_reference_immutable_update
BEFORE UPDATE ON geo_reference
BEGIN SELECT RAISE(ABORT, 'GEO reference is immutable'); END;
CREATE TRIGGER geo_reference_immutable_delete
BEFORE DELETE ON geo_reference
BEGIN SELECT RAISE(ABORT, 'GEO reference is immutable'); END;

-- Post-classification assertions are part of the same atomic migration.
CREATE TEMP TABLE m020_postcheck (check_id TEXT PRIMARY KEY);
CREATE TEMP TRIGGER m020_postcheck_guard
BEFORE INSERT ON m020_postcheck
WHEN (SELECT COUNT(*) FROM geo_reference) <> (SELECT COUNT(*) FROM point_context_revision)
  OR EXISTS (
      SELECT 1 FROM point_context_revision AS context
      LEFT JOIN geo_reference AS geo ON geo.context_revision_id = context.context_revision_id
      WHERE geo.geo_reference_id IS NULL OR context.geo_reference_id <> geo.geo_reference_id
  )
  OR EXISTS (
      SELECT 1 FROM geo_reference
      WHERE availability_state = 'LEGACY_UNCLASSIFIED'
        AND (latitude IS NOT NULL OR longitude IS NOT NULL OR crs_identifier IS NOT NULL
             OR location_provenance_id IS NOT NULL)
  )
  OR EXISTS (
      SELECT 1 FROM m020_legacy_snapshot AS old
      JOIN point_context_revision AS current
        ON current.context_revision_id = old.context_revision_id
      WHERE current.geo_reference IS NOT old.geo_reference
  )
BEGIN SELECT RAISE(ABORT, 'Migration 020 post-classification check failed'); END;
INSERT INTO m020_postcheck VALUES ('complete');
DROP TRIGGER m020_postcheck_guard;
DROP TABLE m020_postcheck;
DROP TABLE m020_legacy_snapshot;
