import enum
import uuid

from db.postgres import Base
from sqlalchemy import JSON, Column, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID


class ChannelEnum(enum.Enum):
    EMAIL = "email"
    WEBSOCKET = "websocket"  # не используем, но предполагаем для будущей реализации


class EventTypesEnum(enum.Enum):
    REGISTRATION = "registration"
    REFRESH_TOKEN_UPDATE = "refresh_token_update"
    SERIES = "series"
    NEW_FILMS = "new_films"
    NEWS = "news"
    PROMOTION = "promotion"
    MOVIE_RECOMMENDATION = "movies_recommendation"
    LIKE_NOTIFICATION = "likes_reviews"


class EventStatusEnum(enum.Enum):
    INIT = "init"
    SUCCESS = "success"
    FAILED = "failed"


class Event(Base):
    __tablename__ = "events"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    data = Column(Text, nullable=True)
    type = Column(Enum(EventTypesEnum), nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    channel = Column(Enum(ChannelEnum), nullable=False)
    send_date = Column(DateTime, nullable=True)  # None - для мгновенных нотификаций
    send_to = Column(JSON, nullable=True)  # None - рассылка всем
    send_from = Column(String, nullable=False)
    status = Column(Enum(EventStatusEnum), nullable=False)
    template = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Event {self.type} {self.id}>"
