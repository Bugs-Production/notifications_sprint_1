from datetime import datetime

from pydantic import BaseModel


class CreateAdminNotificationSchema(BaseModel):
    filter: dict
    type: str
    send_date: datetime
    channel: str
