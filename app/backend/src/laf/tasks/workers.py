import logging
from typing import Dict, Any, Optional

from .celery_app import celery_app
from ..core.database import SessionLocal
from ..models.database import Task, Service
from ..services.clients.k8s_client import KubernetesClient
from ..services.clients.docker_client import DockerClient

logger = logging.getLogger(__name__)


@celery_app.task
def launch_service(
    task_id: int, service_id: int, parameters: Optional[Dict[str, Any]] = None
):
    """Launch a service for a task"""
    db = SessionLocal()
    task = None

    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        service = db.query(Service).filter(Service.id == service_id).first()

        if not task or not service:
            logger.error(
                f"Task or service not found (task_id={task_id}, service_id={service_id})"
            )
            return

        # Merge default parameters with task-specific parameters
        merged_params: Dict[str, str] = {}
        if service.default_parameters is not None:
            merged_params.update(dict(service.default_parameters))  # type: ignore
        if parameters:
            merged_params.update(parameters)

        # Launch based on service type
        service_type = str(service.type)
        service_endpoint = str(service.endpoint)

        if service_type == "kubernetes":
            k8s_client = KubernetesClient()
            job_name = f"task-{task_id}-{service.name.lower()}"
            k8s_client.launch_job(
                job_name=job_name,
                image=service_endpoint,
                env=merged_params,
                namespace="default",
            )
            logger.info(f"Launched Kubernetes job {job_name} for task {task_id}")

        elif service_type == "docker":
            docker_client = DockerClient()
            container_id = docker_client.launch_container(
                image=service_endpoint, env=merged_params
            )
            logger.info(f"Launched Docker container {container_id} for task {task_id}")

        elif service_type == "http":
            import requests

            response = requests.post(service_endpoint, json=merged_params, timeout=30)
            response.raise_for_status()
            logger.info(f"Called HTTP endpoint {service_endpoint} for task {task_id}")

        else:
            logger.error(f"Unknown service type: {service_type}")
            task.status = "failed"  # type: ignore
            db.commit()
            return

        # Update task status to running
        task.status = "running"  # type: ignore
        db.commit()

    except Exception as e:
        logger.error(f"Error launching service: {e}")
        if task:
            task.status = "failed"  # type: ignore
            db.commit()
    finally:
        db.close()
