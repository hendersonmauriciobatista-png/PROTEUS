ALTER TABLE governed_monitoring_point
ADD COLUMN external_station_reference TEXT
CHECK (
    external_station_reference IS NULL
    OR length(trim(external_station_reference)) > 0
);

CREATE UNIQUE INDEX governed_monitoring_point_project_external_station_unique
ON governed_monitoring_point(project_reference, external_station_reference)
WHERE external_station_reference IS NOT NULL;

CREATE TRIGGER point_external_station_reference_immutable
BEFORE UPDATE OF external_station_reference ON governed_monitoring_point
BEGIN
    SELECT RAISE(ABORT, 'external_station_reference is immutable');
END;
