from abc import ABC, abstractmethod
from functools import lru_cache

from db.postgres import get_postgres_session
from fastapi import Depends
from schemas.notification import NOTIFICATION_MAP
from services.exceptions import NotificationNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.send_notification import send_email


class BaseNotificationService(ABC):
    """Абстрактный класс для отправки уведомлений."""

    @abstractmethod
    async def send_email_process(self, event_type: str, event_data: dict) -> None:
        """Отправка сообщений на почту."""
        pass


class NotificationService(BaseNotificationService):
    def __init__(self, postgres_session: AsyncSession):
        self.postgres_session = postgres_session

    async def send_email_process(self, event_type: str, event_data: dict) -> None:
        notification_type = NOTIFICATION_MAP.get(event_type)

        if not notification_type:
            raise NotificationNotFoundError("Notification type not found")

        validate_notification = notification_type(**event_data)

        # отправка email
        send_email.delay(
            event_type=event_type, notification_data=validate_notification.dict()
        )


@lru_cache()
def get_notification_service(
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> NotificationService:
    return NotificationService(postgres_session)
