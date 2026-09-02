ALTER TABLE governed_evaluation ADD COLUMN rule_id TEXT;
ALTER TABLE governed_evaluation ADD COLUMN rule_version INTEGER;
ALTER TABLE governed_evaluation ADD COLUMN rule_payload_hash TEXT;
ALTER TABLE governed_evaluation ADD COLUMN authority_reference_ids TEXT;
ALTER TABLE governed_evaluation ADD COLUMN evidence_reference_ids TEXT;
ALTER TABLE governed_evaluation ADD COLUMN context_revision_id TEXT;
ALTER TABLE governed_evaluation ADD COLUMN aps_set_id TEXT;
ALTER TABLE governed_evaluation ADD COLUMN aps_version INTEGER;
