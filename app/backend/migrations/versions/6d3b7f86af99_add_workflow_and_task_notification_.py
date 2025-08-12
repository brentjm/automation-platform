"""Add workflow and task notification triggers

Revision ID: 6d3b7f86af99
Revises:
Create Date: 2025-08-12 11:08:19.030737

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6d3b7f86af99"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Workflow trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION notify_workflow_changes()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify(
            'workflow_changes',
            json_build_object(
                'workflow_id', NEW.id,
                'operation', TG_OP
            )::text
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    op.execute("""
    CREATE TRIGGER workflow_notify_trigger
    AFTER INSERT OR UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION notify_workflow_changes();
    """)

    # Task trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION notify_task_changes()
    RETURNS TRIGGER AS $$
    BEGIN
        PERFORM pg_notify(
            'task_changes',
            json_build_object(
                'task_id', NEW.id,
                'operation', TG_OP
            )::text
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    op.execute("""
    CREATE TRIGGER task_notify_trigger
    AFTER INSERT OR UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION notify_task_changes();
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS workflow_notify_trigger ON workflows;")
    op.execute("DROP FUNCTION IF EXISTS notify_workflow_changes();")
    op.execute("DROP TRIGGER IF EXISTS task_notify_trigger ON tasks;")
    op.execute("DROP FUNCTION IF EXISTS notify_task_changes();")
