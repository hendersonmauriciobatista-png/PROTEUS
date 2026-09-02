DROP TRIGGER context_revision_immutable_update;
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
)
BEGIN SELECT RAISE(ABORT, 'point_context_revision immutable outside authorized close'); END;
