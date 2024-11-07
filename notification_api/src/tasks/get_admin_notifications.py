import logging

from celery import shared_task
from db.sync_postgres import get_sync_session
from models.admin import NotificationTask, NotificationTaskStatusEnum
from sqlalchemy import func, select

logger = logging.getLogger()


@shared_task
def get_admin_notifications() -> None:
    logger.info("Executing scheduled task")
    with get_sync_session() as session:
        stmt = select(NotificationTask).where(
            NotificationTask.status == NotificationTaskStatusEnum.INIT
        )
        result = session.scalars(stmt)
        for row in result.all():
            row.status = NotificationTaskStatusEnum.IN_PROGRESS
            row.updated_at = func.now()
            session.commit()
            logger.info(row)
