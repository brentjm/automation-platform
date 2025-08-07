import psycopg2
import psycopg2.extensions
import json
import requests
import logging

from .tasks import run_instrument_task
from .models import db, Workflow, Task
from laf.tasks import celery, run_instrument_task

logger = logging.getLogger(__name__)


class WebhookHandler:
    def __init__(self, app):
        self.app = app
        self.db_config = {
            "host": app.config.get("DB_HOST", "localhost"),
            "port": app.config.get("DB_PORT", 5432),
            "database": app.config.get("DB_NAME", "laf"),
            "user": app.config.get("DB_USER", "postgres"),
            "password": app.config.get("DB_PASSWORD", "password"),
        }

    def start_listener(self):
        """Start listening for PostgreSQL notifications"""
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            cur = conn.cursor()
            cur.execute("LISTEN workflow_changes;")
            cur.execute("LISTEN task_changes;")

            logger.info("Started PostgreSQL notification listener")

            while True:
                if conn.poll() == psycopg2.extensions.POLL_OK:
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        self.handle_notification(notify.channel, notify.payload)

        except Exception as e:
            logger.error(f"Database listener error: {e}")

    def handle_notification(self, channel, payload):
        """Handle PostgreSQL notifications"""
        try:
            data = json.loads(payload) if payload else {}

            if channel == "workflow_changes":
                self.handle_workflow_change(data)
            elif channel == "task_changes":
                self.handle_task_change(data)

        except Exception as e:
            logger.error(f"Error handling notification: {e}")

    def handle_workflow_change(self, data):
        """Handle workflow status changes"""
        with self.app.app_context():
            workflow_id = data.get("workflow_id")
            operation = data.get("operation", "UPDATE")

            if operation == "INSERT":
                # Start the first task when workflow is created
                self.start_first_task(workflow_id)
            elif operation == "UPDATE":
                # Handle workflow status updates
                self.process_workflow_update(workflow_id, data)

    def process_workflow_update(self, workflow_id, data):
        """Stub for workflow update logic (extend as needed)."""
        pass

    def handle_task_change(self, data):
        """Handle task status changes"""
        with self.app.app_context():
            task_id = data.get("task_id")
            operation = data.get("operation", "UPDATE")

            if operation == "UPDATE":
                self.process_task_update(task_id, data)

    def start_first_task(self, workflow_id):
        """Start the first task in a workflow"""
        try:
            first_task = (
                Task.query.filter_by(workflow_id=workflow_id)
                .order_by(Task.order_index)
                .first()
            )

            if first_task:
                self.trigger_instrument_service(first_task)

        except Exception as e:
            logger.error(f"Error starting first task: {e}")

    def process_task_update(self, task_id, data):
        """Process task status updates and trigger next task if needed"""
        try:
            task = Task.query.get(task_id)
            if not task:
                return

            # If task completed, start next task
            if task.status == "completed":
                self.start_next_task(task)
            elif task.status == "running":
                # Update workflow status to running
                workflow = task.workflow
                if workflow.status == "pending":
                    workflow.status = "running"
                    db.session.commit()

        except Exception as e:
            logger.error(f"Error processing task update: {e}")

    def start_next_task(self, completed_task):
        """Start the next task in the workflow"""
        try:
            next_task = (
                Task.query.filter_by(workflow_id=completed_task.workflow_id)
                .filter(Task.order_index > completed_task.order_index)
                .order_by(Task.order_index)
                .first()
            )

            if next_task:
                self.trigger_instrument_service(next_task)
            else:
                # No more tasks, mark workflow as completed
                workflow = completed_task.workflow
                workflow.status = "completed"
                db.session.commit()

        except Exception as e:
            logger.error(f"Error starting next task: {e}")

    def trigger_instrument_service(self, task):
        """Trigger the instrument service for a task"""
        try:
            # Use apply_async as an alternative to delay
            run_instrument_task.delay(task.id, task.instrument)
            logger.info(
                f"Triggered Celery task for instrument {task.instrument} and task {task.id}"
            )

            # Update task status to running
            task.status = "running"
            db.session.commit()

        except Exception as e:
            logger.error(f"Error triggering instrument service: {e}")
            # Mark task as failed
            task.status = "failed"
            db.session.commit()
