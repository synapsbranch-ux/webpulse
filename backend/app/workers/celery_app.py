from celery import Celery
from app.config import settings

celery_app = Celery(
    "synapsbranch",
    broker=str(settings.REDIS_URL),
    backend=str(settings.REDIS_URL),
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True
)
