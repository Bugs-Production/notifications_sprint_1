from celery import Celery, bootsteps
from core.config import settings
from kombu import Exchange, Queue

default_queue_name = "default"
default_exchange_name = "default"
default_routing_key = "default"
deadletter_suffix = "deadletter"
deadletter_queue_name = default_queue_name + f".{deadletter_suffix}"
deadletter_exchange_name = default_exchange_name + f".{deadletter_suffix}"
deadletter_routing_key = default_routing_key + f".{deadletter_suffix}"


class DeclareDLXnDLQ(bootsteps.StartStopStep):

    requires = {"celery.worker.components:Pool"}

    def start(self, worker):
        app = worker.app

        # Declare DLX and DLQ
        dlx = Exchange(deadletter_exchange_name, type="direct")

        dead_letter_queue = Queue(
            name=deadletter_queue_name, exchange=dlx, routing_key=deadletter_routing_key
        )

        with worker.app.pool.acquire() as conn:
            dead_letter_queue.bind(conn).declare()


default_exchange = Exchange(name=default_exchange_name, type="direct")
default_queue = Queue(
    name=default_queue_name,
    exchange=default_exchange,
    routing_key=default_routing_key,
    queue_arguments={
        "x-dead-letter-exchange": deadletter_exchange_name,
        "x-dead-letter-routing-key": deadletter_routing_key,
    },
)

celery_app = Celery(settings.project_name, broker=settings.broker_url)

# Add steps to workers that declare DLX and DLQ if they don't exist
celery_app.steps["worker"].add(DeclareDLXnDLQ)

celery_app.conf.update(
    imports=["tasks.send_notification", "tasks.get_admin_notifications"],
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    beat_schedule={
        "admin_notifications": {
            "task": "tasks.get_admin_notifications.get_admin_notifications",
            "schedule": settings.celery_scheduler_interval_sec,
        }
    },
    task_queues=(default_queue,),
    task_default_queue=default_queue_name,
    task_default_exchange=default_exchange_name,
    task_default_routing_key=default_routing_key,
)
