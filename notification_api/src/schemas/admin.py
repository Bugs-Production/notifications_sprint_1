from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateAdminNotificationSchema(BaseModel):
    filter: dict
    type: str
    send_date: datetime
    channel: str


class GetAdminNotificationSchema(BaseModel):
    id: UUID
    type: str
    channel: str
    status: str
    created_at: datetime
    send_date: datetime

    class Config:
        orm_mode = True
