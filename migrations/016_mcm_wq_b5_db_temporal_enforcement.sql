-- B5/016 candidate: database-level temporal enforcement.
-- This file is a migration body only; schema-version registration remains the
-- responsibility of the migration runner that will eventually install 016.

-- Part 1: fatal, read-only preflight for all governed comparison timestamps.
CREATE TEMP TABLE b5_temporal_preflight (
    source_table TEXT,
    source_column TEXT,
    row_id TEXT,
    value
);

CREATE TEMP TRIGGER b5_temporal_preflight_guard
BEFORE INSERT ON b5_temporal_preflight
WHEN NEW.value IS NULL
  OR NOT (
      typeof(NEW.value) = 'text'
      AND length(NEW.value) = 27
      AND length(CAST(NEW.value AS BLOB)) = 27
      AND hex(CAST(NEW.value AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
      AND CAST(substr(NEW.value, 1, 4) AS INTEGER) BETWEEN 1 AND 9999
      AND CAST(substr(NEW.value, 6, 2) AS INTEGER) BETWEEN 1 AND 12
      AND CAST(substr(NEW.value, 9, 2) AS INTEGER) BETWEEN 1 AND
          CASE CAST(substr(NEW.value, 6, 2) AS INTEGER)
              WHEN 2 THEN
                  CASE
                      WHEN CAST(substr(NEW.value, 1, 4) AS INTEGER) % 400 = 0
                        OR (
                            CAST(substr(NEW.value, 1, 4) AS INTEGER) % 4 = 0
                            AND CAST(substr(NEW.value, 1, 4) AS INTEGER) % 100 <> 0
                        )
                      THEN 29
                      ELSE 28
                  END
              WHEN 4 THEN 30
              WHEN 6 THEN 30
              WHEN 9 THEN 30
              WHEN 11 THEN 30
              ELSE 31
          END
      AND CAST(substr(NEW.value, 12, 2) AS INTEGER) BETWEEN 0 AND 23
      AND CAST(substr(NEW.value, 15, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.value, 18, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.value, 21, 6) AS INTEGER) BETWEEN 0 AND 999999
  )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 canonical temporal preflight failed');
END;

INSERT INTO b5_temporal_preflight (source_table, source_column, row_id, value)
SELECT 'authority_applicability', 'effective_from', CAST(rowid AS TEXT), effective_from
FROM authority_applicability
UNION ALL
SELECT 'authority_applicability_event', 'effective_at', CAST(rowid AS TEXT), effective_at
FROM authority_applicability_event
UNION ALL
SELECT 'governed_measurement', 'measured_at', CAST(rowid AS TEXT), measured_at
FROM governed_measurement;

-- Part 1b: reject invalid derived intervals and pre-existing true overlap.
CREATE TEMP TABLE b5_interval_preflight (
    violation TEXT,
    applicability_id TEXT,
    conflicting_applicability_id TEXT
);

CREATE TEMP TRIGGER b5_interval_preflight_guard
BEFORE INSERT ON b5_interval_preflight
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 applicability interval preflight failed');
END;

INSERT INTO b5_interval_preflight
    (violation, applicability_id, conflicting_applicability_id)
SELECT 'terminal_before_start', applicability_id, NULL
FROM authority_applicability_temporal
WHERE terminal_effective_at IS NOT NULL
  AND terminal_effective_at < effective_from
UNION ALL
SELECT 'true_overlap', left_interval.applicability_id,
       right_interval.applicability_id
FROM authority_applicability_temporal AS left_interval
JOIN authority_applicability_temporal AS right_interval
  ON left_interval.applicability_id < right_interval.applicability_id
 AND left_interval.context_revision_id = right_interval.context_revision_id
 AND left_interval.parameter_reference = right_interval.parameter_reference
WHERE (left_interval.terminal_effective_at IS NULL
       OR left_interval.terminal_effective_at > left_interval.effective_from)
  AND (right_interval.terminal_effective_at IS NULL
       OR right_interval.terminal_effective_at > right_interval.effective_from)
  AND (right_interval.terminal_effective_at IS NULL
       OR left_interval.effective_from < right_interval.terminal_effective_at)
  AND (left_interval.terminal_effective_at IS NULL
       OR right_interval.effective_from < left_interval.terminal_effective_at);

DROP TRIGGER b5_interval_preflight_guard;
DROP TABLE b5_interval_preflight;
DROP TRIGGER b5_temporal_preflight_guard;
DROP TABLE b5_temporal_preflight;

-- Part 2: future applicability rows are validated as open-ended at insertion.
CREATE TRIGGER b5_authority_applicability_effective_from_canonical
BEFORE INSERT ON authority_applicability
WHEN NEW.effective_from IS NULL
  OR NOT (
      typeof(NEW.effective_from) = 'text'
      AND length(NEW.effective_from) = 27
      AND length(CAST(NEW.effective_from AS BLOB)) = 27
      AND hex(CAST(NEW.effective_from AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
      AND CAST(substr(NEW.effective_from, 1, 4) AS INTEGER) BETWEEN 1 AND 9999
      AND CAST(substr(NEW.effective_from, 6, 2) AS INTEGER) BETWEEN 1 AND 12
      AND CAST(substr(NEW.effective_from, 9, 2) AS INTEGER) BETWEEN 1 AND
          CASE CAST(substr(NEW.effective_from, 6, 2) AS INTEGER)
              WHEN 2 THEN
                  CASE
                      WHEN CAST(substr(NEW.effective_from, 1, 4) AS INTEGER) % 400 = 0
                        OR (
                            CAST(substr(NEW.effective_from, 1, 4) AS INTEGER) % 4 = 0
                            AND CAST(substr(NEW.effective_from, 1, 4) AS INTEGER) % 100 <> 0
                        )
                      THEN 29
                      ELSE 28
                  END
              WHEN 4 THEN 30
              WHEN 6 THEN 30
              WHEN 9 THEN 30
              WHEN 11 THEN 30
              ELSE 31
          END
      AND CAST(substr(NEW.effective_from, 12, 2) AS INTEGER) BETWEEN 0 AND 23
      AND CAST(substr(NEW.effective_from, 15, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.effective_from, 18, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.effective_from, 21, 6) AS INTEGER) BETWEEN 0 AND 999999
  )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 canonical effective_from required');
END;

CREATE TRIGGER b5_authority_applicability_no_true_overlap
BEFORE INSERT ON authority_applicability
WHEN EXISTS (
    SELECT 1
    FROM authority_applicability_temporal AS existing_interval
    WHERE existing_interval.context_revision_id = NEW.context_revision_id
      AND existing_interval.parameter_reference = NEW.parameter_reference
      AND (
          existing_interval.terminal_effective_at IS NULL
          OR existing_interval.terminal_effective_at > existing_interval.effective_from
      )
      AND (
          existing_interval.terminal_effective_at IS NULL
          OR NEW.effective_from < existing_interval.terminal_effective_at
      )
)
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 applicability temporal overlap blocked');
END;

-- Part 3: event effective_at is canonical and terminal intervals are valid.
CREATE TRIGGER b5_authority_applicability_event_effective_at_canonical
BEFORE INSERT ON authority_applicability_event
WHEN NEW.effective_at IS NULL
  OR NOT (
      typeof(NEW.effective_at) = 'text'
      AND length(NEW.effective_at) = 27
      AND length(CAST(NEW.effective_at AS BLOB)) = 27
      AND hex(CAST(NEW.effective_at AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
      AND CAST(substr(NEW.effective_at, 1, 4) AS INTEGER) BETWEEN 1 AND 9999
      AND CAST(substr(NEW.effective_at, 6, 2) AS INTEGER) BETWEEN 1 AND 12
      AND CAST(substr(NEW.effective_at, 9, 2) AS INTEGER) BETWEEN 1 AND
          CASE CAST(substr(NEW.effective_at, 6, 2) AS INTEGER)
              WHEN 2 THEN
                  CASE
                      WHEN CAST(substr(NEW.effective_at, 1, 4) AS INTEGER) % 400 = 0
                        OR (
                            CAST(substr(NEW.effective_at, 1, 4) AS INTEGER) % 4 = 0
                            AND CAST(substr(NEW.effective_at, 1, 4) AS INTEGER) % 100 <> 0
                        )
                      THEN 29
                      ELSE 28
                  END
              WHEN 4 THEN 30
              WHEN 6 THEN 30
              WHEN 9 THEN 30
              WHEN 11 THEN 30
              ELSE 31
          END
      AND CAST(substr(NEW.effective_at, 12, 2) AS INTEGER) BETWEEN 0 AND 23
      AND CAST(substr(NEW.effective_at, 15, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.effective_at, 18, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.effective_at, 21, 6) AS INTEGER) BETWEEN 0 AND 999999
  )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 canonical effective_at required');
END;

CREATE TRIGGER b5_authority_applicability_event_terminal_time
BEFORE INSERT ON authority_applicability_event
WHEN NEW.event_type IN ('REVOKED', 'SUPERSEDED')
 AND EXISTS (
     SELECT 1
     FROM authority_applicability AS target
     WHERE target.applicability_id = NEW.applicability_id
       AND NEW.effective_at < target.effective_from
 )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 terminal effective_at precedes applicability start');
END;

CREATE TRIGGER b5_authority_applicability_event_terminal_no_overlap
BEFORE INSERT ON authority_applicability_event
WHEN NEW.event_type IN ('REVOKED', 'SUPERSEDED')
 AND EXISTS (
     SELECT 1
     FROM authority_applicability AS target
     JOIN authority_applicability_temporal AS other_interval
       ON other_interval.applicability_id <> target.applicability_id
      AND other_interval.context_revision_id = target.context_revision_id
      AND other_interval.parameter_reference = target.parameter_reference
     WHERE target.applicability_id = NEW.applicability_id
       AND NEW.effective_at > target.effective_from
       AND (
           other_interval.terminal_effective_at IS NULL
           OR other_interval.terminal_effective_at > other_interval.effective_from
       )
       AND (
           other_interval.terminal_effective_at IS NULL
           OR target.effective_from < other_interval.terminal_effective_at
       )
       AND other_interval.effective_from < NEW.effective_at
 )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 terminal temporal overlap blocked');
END;

CREATE TRIGGER b5_authority_applicability_event_no_retroactive_evaluation
BEFORE INSERT ON authority_applicability_event
WHEN NEW.event_type IN ('REVOKED', 'SUPERSEDED')
 AND EXISTS (
     SELECT 1
     FROM authority_applicability AS target
     JOIN governed_measurement AS measurement
       ON measurement.context_revision_id = target.context_revision_id
      AND measurement.parameter_reference = target.parameter_reference
     JOIN governed_evaluation AS evaluation
       ON evaluation.measurement_id = measurement.measurement_id
      AND evaluation.parameter_reference = target.parameter_reference
     WHERE target.applicability_id = NEW.applicability_id
       AND measurement.measured_at >= target.effective_from
       AND measurement.measured_at < NEW.effective_at
 )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 retroactive governed evaluation impact blocked');
END;

-- Part 4: direct SQL measurement writes use the same canonical grammar.
CREATE TRIGGER b5_governed_measurement_measured_at_canonical
BEFORE INSERT ON governed_measurement
WHEN NEW.measured_at IS NULL
  OR NOT (
      typeof(NEW.measured_at) = 'text'
      AND length(NEW.measured_at) = 27
      AND length(CAST(NEW.measured_at AS BLOB)) = 27
      AND hex(CAST(NEW.measured_at AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
      AND CAST(substr(NEW.measured_at, 1, 4) AS INTEGER) BETWEEN 1 AND 9999
      AND CAST(substr(NEW.measured_at, 6, 2) AS INTEGER) BETWEEN 1 AND 12
      AND CAST(substr(NEW.measured_at, 9, 2) AS INTEGER) BETWEEN 1 AND
          CASE CAST(substr(NEW.measured_at, 6, 2) AS INTEGER)
              WHEN 2 THEN
                  CASE
                      WHEN CAST(substr(NEW.measured_at, 1, 4) AS INTEGER) % 400 = 0
                        OR (
                            CAST(substr(NEW.measured_at, 1, 4) AS INTEGER) % 4 = 0
                            AND CAST(substr(NEW.measured_at, 1, 4) AS INTEGER) % 100 <> 0
                        )
                      THEN 29
                      ELSE 28
                  END
              WHEN 4 THEN 30
              WHEN 6 THEN 30
              WHEN 9 THEN 30
              WHEN 11 THEN 30
              ELSE 31
          END
      AND CAST(substr(NEW.measured_at, 12, 2) AS INTEGER) BETWEEN 0 AND 23
      AND CAST(substr(NEW.measured_at, 15, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.measured_at, 18, 2) AS INTEGER) BETWEEN 0 AND 59
      AND CAST(substr(NEW.measured_at, 21, 6) AS INTEGER) BETWEEN 0 AND 999999
  )
BEGIN
    SELECT RAISE(ROLLBACK, 'B5 canonical measured_at required');
END;
