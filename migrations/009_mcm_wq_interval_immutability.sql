CREATE TRIGGER context_temporal_immutable_closed BEFORE UPDATE OF effective_from,effective_until,point_id ON point_context_revision
WHEN OLD.effective_until IS NOT NULL AND (NEW.effective_from IS NOT OLD.effective_from OR NEW.effective_until IS NOT OLD.effective_until OR NEW.point_id IS NOT OLD.point_id)
BEGIN SELECT RAISE(ABORT,'closed context interval is immutable'); END;
CREATE TRIGGER aps_temporal_immutable_closed BEFORE UPDATE OF effective_from,effective_until,context_revision_id,aps_set_id,aps_version ON aps_temporal_applicability
WHEN OLD.effective_until IS NOT NULL AND (NEW.effective_from IS NOT OLD.effective_from OR NEW.effective_until IS NOT OLD.effective_until OR NEW.context_revision_id IS NOT OLD.context_revision_id OR NEW.aps_set_id IS NOT OLD.aps_set_id OR NEW.aps_version IS NOT OLD.aps_version)
BEGIN SELECT RAISE(ABORT,'closed APS interval is immutable'); END;
CREATE TRIGGER aps_temporal_no_delete BEFORE DELETE ON aps_temporal_applicability BEGIN SELECT RAISE(ABORT,'APS temporal history is immutable'); END;
CREATE TRIGGER context_temporal_no_delete BEFORE DELETE ON point_context_revision BEGIN SELECT RAISE(ABORT,'context temporal history is immutable'); END;
