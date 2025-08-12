-- Database triggers and functions for PostgreSQL notifications

-- Function to notify workflow changes
CREATE OR REPLACE FUNCTION notify_workflow_changes()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('workflow_changes', json_build_object(
        'operation', TG_OP,
        'workflow_id', COALESCE(NEW.id, OLD.id),
        'status', CASE WHEN NEW IS NOT NULL THEN NEW.status ELSE NULL END,
        'old_status', CASE WHEN OLD IS NOT NULL THEN OLD.status ELSE NULL END
    )::text);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Function to notify task changes
CREATE OR REPLACE FUNCTION notify_task_changes()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('task_changes', json_build_object(
        'operation', TG_OP,
        'task_id', COALESCE(NEW.id, OLD.id),
        'workflow_id', COALESCE(NEW.workflow_id, OLD.workflow_id),
        'status', CASE WHEN NEW IS NOT NULL THEN NEW.status ELSE NULL END,
        'old_status', CASE WHEN OLD IS NOT NULL THEN OLD.status ELSE NULL END,
        'instrument', CASE WHEN NEW IS NOT NULL THEN NEW.instrument ELSE NULL END
    )::text);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Triggers for workflow table
DROP TRIGGER IF EXISTS workflow_changes_trigger ON workflow;
CREATE TRIGGER workflow_changes_trigger
    AFTER INSERT OR UPDATE OR DELETE ON workflow
    FOR EACH ROW
    EXECUTE FUNCTION notify_workflow_changes();

-- Triggers for task table
DROP TRIGGER IF EXISTS task_changes_trigger ON task;
CREATE TRIGGER task_changes_trigger
    AFTER INSERT OR UPDATE OR DELETE ON task
    FOR EACH ROW
    EXECUTE FUNCTION notify_task_changes();

-- Index for better performance
CREATE INDEX IF NOT EXISTS idx_task_workflow_order ON task(workflow_id, order_index);
CREATE INDEX IF NOT EXISTS idx_task_status ON task(status);
CREATE INDEX IF NOT EXISTS idx_workflow_status ON workflow(status);
