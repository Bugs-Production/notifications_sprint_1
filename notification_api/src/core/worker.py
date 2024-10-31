from celery import Celery
from core.config import settings

celery_app = Celery(settings.project_name, broker=settings.broker_url)

celery_app.conf.update(
    imports=["tasks.send_notification"],
    broker_connection_retry_on_startup=True,
    task_track_started=True,
)
