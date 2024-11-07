from celery import Celery
from celery.schedules import crontab
from core.config import settings

celery_app = Celery(settings.project_name, broker=settings.broker_url)

celery_app.conf.update(
    imports=["tasks.send_notification", "tasks.get_admin_notifications"],
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    beat_schedule={
        "admin_notifications": {
            "task": "tasks.get_admin_notifications.get_admin_notifications",
            "schedule": crontab(),
        }
    },
)
