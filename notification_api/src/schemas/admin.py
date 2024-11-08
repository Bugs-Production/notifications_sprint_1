from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateNotificationSchema(BaseModel):
    filter: dict
    type: str
    send_date: datetime | None = None
    channel: str


class GetNotificationSchema(BaseModel):
    id: UUID
    type: str
    channel: str
    status: str
    created_at: datetime
    send_date: datetime

    class Config:
        """Используем режим ORM для корректного преобразования модели из SQLAlchemy."""

        orm_mode = True


class UpdateNotificationSchema(BaseModel):
    send_date: datetime
