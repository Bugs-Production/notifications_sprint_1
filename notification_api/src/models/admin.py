import enum
import uuid

from db.postgres import Base
from models.event import ChannelEnum, EventTypesEnum
from sqlalchemy import JSON, Column, DateTime, func
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.dialects.postgresql import UUID


class NotificationTaskStatusEnum(enum.Enum):
    INIT = "init"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"


class NotificationTask(Base):
    __tablename__ = "admin_notifications"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    type = Column(pg.ENUM(EventTypesEnum), nullable=False)
    channel = Column(pg.ENUM(ChannelEnum), nullable=False)
    filter = Column(JSON, nullable=False)
    status = Column(pg.ENUM(NotificationTaskStatusEnum), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    send_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<NotificationTask {self.type} {self.id}>"
