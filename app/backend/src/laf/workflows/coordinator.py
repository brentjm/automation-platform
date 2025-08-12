import logging
from sqlalchemy.orm import Session

from ..core.database import SessionLocal
from ..models.database import Task, Service
from ..tasks.workers import launch_service

logger = logging.getLogger(__name__)


class WorkflowCoordinator:
    def __init__(self):
        pass

    def get_db(self) -> Session:
        return SessionLocal()

    def handle_workflow_change(self, data: dict):
        """Handle workflow status changes"""
        db = self.get_db()
        try:
            workflow_id = data.get("workflow_id")
            operation = data.get("operation", "UPDATE")

            if operation == "INSERT":
                self.start_first_task(workflow_id, db)
            elif operation == "UPDATE":
                self.process_workflow_update(workflow_id, data, db)
        finally:
            db.close()

    def process_workflow_update(self, workflow_id: int, data: dict, db: Session):
        """Process workflow update logic"""
        # Extend as needed
        pass

    def handle_task_change(self, data: dict):
        """Handle task status changes"""
        db = self.get_db()
        try:
            task_id = data.get("task_id")
            operation = data.get("operation", "UPDATE")

            if operation == "UPDATE":
                self.process_task_update(task_id, data, db)
        finally:
            db.close()

    def get_service(self, task: Task, db: Session) -> Service:
        """Fetch the Service for a given task's service mapping"""
        service = (
            db.query(Service)
            .filter(Service.id == task.service_id, Service.enabled == True)
            .first()
        )

        if not service:
            logger.error(f"No enabled service found for service_id {task.service_id}")
        return service

    def start_first_task(self, workflow_id: int, db: Session):
        """Start the first task in a workflow"""
        try:
            first_task = (
                db.query(Task)
                .filter(Task.workflow_id == workflow_id)
                .order_by(Task.order_index)
                .first()
            )

            if first_task:
                service = self.get_service(first_task, db)
                if service:
                    launch_service.apply_async(
                        args=[first_task.id, service.id, first_task.service_parameters]
                    )
        except Exception as e:
            logger.error(f"Error starting first task: {e}")

    def process_task_update(self, task_id: int, data: dict, db: Session):
        """Process task status updates and trigger next task if needed"""
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return

            # If task completed, start next task
            if task.status == "completed":
                self.start_next_task(task, db)
            elif task.status == "running":
                # Update workflow status to running
                workflow = task.workflow
                if workflow.status == "pending":
                    workflow.status = "running"
                    db.commit()
        except Exception as e:
            logger.error(f"Error processing task update: {e}")

    def start_next_task(self, completed_task: Task, db: Session):
        """Start the next task in the workflow"""
        try:
            next_task = (
                db.query(Task)
                .filter(Task.workflow_id == completed_task.workflow_id)
                .filter(Task.order_index > completed_task.order_index)
                .order_by(Task.order_index)
                .first()
            )

            if next_task:
                service = self.get_service(next_task, db)
                if service:
                    launch_service.apply_async(
                        args=[next_task.id, service.id, next_task.service_parameters]
                    )
            else:
                # No more tasks, mark workflow as completed
                workflow = completed_task.workflow
                workflow.status = "completed"
                db.commit()
        except Exception as e:
            logger.error(f"Error starting next task: {e}")
