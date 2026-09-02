CREATE UNIQUE INDEX governed_measurement_identity_unique ON governed_measurement(measurement_id, parameter_reference);
CREATE TABLE governed_evaluation (
    evaluation_id TEXT PRIMARY KEY,
    measurement_id TEXT NOT NULL REFERENCES governed_measurement(measurement_id) ON DELETE RESTRICT,
    parameter_reference TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('NORMAL','ATENCAO','CRITICO','NAO_AVALIAVEL')),
    message TEXT NOT NULL,
    rule_origin TEXT NOT NULL,
    evaluated_at TEXT NOT NULL,
    registered_at TEXT NOT NULL,
    evaluation_engine TEXT NOT NULL,
    evaluation_engine_version TEXT NOT NULL,
    explanation_data TEXT,
    FOREIGN KEY (measurement_id, parameter_reference)
      REFERENCES governed_measurement(measurement_id, parameter_reference)
);
CREATE INDEX governed_evaluation_measurement_idx ON governed_evaluation(measurement_id);
CREATE TRIGGER governed_evaluation_immutable_update BEFORE UPDATE ON governed_evaluation BEGIN
  SELECT RAISE(ABORT, 'governed_evaluation is immutable');
END;
CREATE TRIGGER governed_evaluation_immutable_delete BEFORE DELETE ON governed_evaluation BEGIN
  SELECT RAISE(ABORT, 'governed_evaluation deletion is not authorized');
END;
