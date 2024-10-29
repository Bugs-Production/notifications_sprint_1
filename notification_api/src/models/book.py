import uuid

from db.postgres import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class Book(Base):
    __tablename__ = "books"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title = Column(String(50), unique=True, nullable=False)
