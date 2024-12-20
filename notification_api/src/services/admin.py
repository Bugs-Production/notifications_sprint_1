from datetime import datetime
from functools import lru_cache

from db.postgres import get_postgres_session
from fastapi import Depends
from models.admin import NotificationTask, NotificationTaskStatusEnum
from models.event import ChannelEnum, EventTypesEnum
from schemas import admin as admin_schemas
from services import exceptions as exc
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AdminNotificationService:
    def __init__(self, postgres_session: AsyncSession):
        self.postgres_session = postgres_session

    async def add_notification_task(
        self, notification_data: admin_schemas.CreateNotificationSchema
    ) -> NotificationTask:
        try:
            notification_type = EventTypesEnum(notification_data.type)
        except ValueError:
            raise exc.NotificationNotFoundError("Notification type not found")

        try:
            channel = ChannelEnum(notification_data.channel)
        except ValueError:
            raise exc.ChannelNotFoundError("Channel not found")

        send_date = notification_data.send_date.replace(tzinfo=None)

        if not send_date:
            send_date = func.now()

        task = NotificationTask(
            status=NotificationTaskStatusEnum.INIT,
            filter=notification_data.filter,
            type=notification_type,
            channel=channel,
            send_date=send_date,
        )

        async with self.postgres_session() as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task

    async def get_notifications_list(self) -> NotificationTask | None:
        async with self.postgres_session() as session:
            notifications_data = await session.scalars(select(NotificationTask))
            return notifications_data.all()

    async def update_notification(
        self,
        notification_id: str,
        notification_data: admin_schemas.UpdateNotificationSchema,
    ) -> NotificationTask | None:
        async with self.postgres_session() as session:
            notifications_data = await session.scalars(
                select(NotificationTask).filter_by(id=notification_id)
            )
            notification = notifications_data.first()

            if notification is None:
                raise exc.NotificationNotFoundError("Notification not found")

            for field in notification_data.model_fields_set:
                field_value = getattr(notification_data, field)
                if isinstance(field_value, datetime):
                    field_value = field_value.replace(tzinfo=None)
                setattr(notification, field, field_value)
            try:
                await session.commit()
            except IntegrityError:
                raise exc.ConflictError("ConflictError")
            return notification

    async def delete_notification_task(self, notification_id: str):
        async with self.postgres_session() as session:
            notifications_data = await session.scalars(
                select(NotificationTask).filter_by(id=notification_id)
            )
            notification = notifications_data.first()

            if notification is None:
                raise exc.NotificationNotFoundError("Notification not found")

            await session.delete(notification)
            await session.commit()


@lru_cache()
def get_admin_notification_service(
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> AdminNotificationService:
    return AdminNotificationService(postgres_session)
