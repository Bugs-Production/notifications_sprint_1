import logging

from celery import shared_task
from db.sync_postgres import get_sync_session
from models.admin import NotificationTask, NotificationTaskStatusEnum
from sqlalchemy import func, select
from tasks.send_notification import send_mass_email

logger = logging.getLogger()


def update_task_status(
    task: NotificationTask, status: NotificationTaskStatusEnum, session
):
    task.status = status
    task.updated_at = func.now()
    session.commit()


@shared_task
def get_admin_notifications() -> None:
    logger.info("Executing scheduled task")
    with get_sync_session() as session:
        time_now = func.now()
        stmt = select(NotificationTask).where(
            NotificationTask.status == NotificationTaskStatusEnum.INIT,
            NotificationTask.send_date <= time_now,
        )
        notifications_data = session.scalars(stmt)

        for row in notifications_data.all():
            try:
                update_task_status(row, NotificationTaskStatusEnum.IN_PROGRESS, session)
                send_mass_email.delay(
                    event_type=row.type.value, notification_data=row.filter
                )
                update_task_status(row, NotificationTaskStatusEnum.SUCCESS, session)
            except Exception as exc:
                logger.error(exc)
                update_task_status(row, NotificationTaskStatusEnum.FAILED, session)
