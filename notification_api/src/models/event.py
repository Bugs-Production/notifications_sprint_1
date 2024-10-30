from sqlalchemy import Column, DateTime, String, func, Text, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
import enum

import uuid

from db.postgres import Base


class ChannelEnum(enum.Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket" # не используем, но предполагаем для будущей реализации

class EventTypesEnum(enum.Enum):
    REGISTRATION = "registration"
    REFRESH_TOKEN_UPDATE = "refresh_token_update"
    LIKE = "like"
    SERIES = "series"
    NEW_FILMS = "new_films"
    NEWS = "news"
    SALE = "sale"
    PROMOTION = "promotion"

class EventStatusEnum(enum.Enum):
    INIT = "init"
    SUCCESS = "success"
    FAILED = "failed"

class Event(Base):
    __tablename__ = 'events'
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    data = Column(Text, nullable=False)
    type = Column(Enum(EventTypesEnum), nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    channel = Column(Enum(ChannelEnum), nullable=False)
    send_date = Column(DateTime, nullable=True)    # None - для мгновенных нотификаций
    send_to = Column(JSON, nullable=True)  # None - рассылка всем
    send_from = Column(String, nullable=False)
    status = Column(Enum(EventStatusEnum), nullable=False)
    template = Column(String(200), nullable=False)

    def __repr__(self) -> str:
        return f"<Event {self.type} {self.id}>"
