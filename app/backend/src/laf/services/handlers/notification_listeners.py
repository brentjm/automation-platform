import json
import logging
import psycopg2
import psycopg2.extensions
from typing import Dict, Any

from ...core.config import settings
from ...workflows.coordinator import WorkflowCoordinator

logger = logging.getLogger(__name__)


class NotificationListener:
    def __init__(self):
        self.coordinator = WorkflowCoordinator()
        self.connection = None

    def connect(self):
        """Connect to PostgreSQL and listen for notifications"""
        try:
            self.connection = psycopg2.connect(settings.database_url)
            self.connection.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
            )
            logger.info("Connected to PostgreSQL for notifications")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def start_listener(self):
        """Start listening for database notifications"""
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()

        try:
            # Listen for workflow and task changes
            cursor.execute("LISTEN workflow_changes;")
            cursor.execute("LISTEN task_changes;")
            logger.info("Started listening for database notifications")

            while True:
                if self.connection.notifies:
                    self.connection.poll()

                    while self.connection.notifies:
                        notify = self.connection.notifies.pop(0)
                        self.handle_notification(notify)
                else:
                    # Wait for notifications
                    self.connection.poll()

        except Exception as e:
            logger.error(f"Error in notification listener: {e}")
        finally:
            cursor.close()

    def handle_notification(self, notify):
        """Handle incoming notifications"""
        try:
            channel = notify.channel
            payload = json.loads(notify.payload) if notify.payload else {}

            logger.info(f"Received notification on channel {channel}: {payload}")

            if channel == "workflow_changes":
                self.coordinator.handle_workflow_change(payload)
            elif channel == "task_changes":
                self.coordinator.handle_task_change(payload)

        except Exception as e:
            logger.error(f"Error handling notification: {e}")
