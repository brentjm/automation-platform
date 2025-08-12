from celery import Celery

from ..core.config import settings

celery_app = Celery(
    "laf",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["laf.tasks.workers"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
