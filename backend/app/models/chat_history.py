import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    session_id = Column(
        String(100),
        nullable=False,
    )

    user_message = Column(
        Text,
        nullable=False,
    )

    ai_response = Column(
        Text,
        nullable=False,
    )

    token_usage = Column(
        Integer,
        default=0,
        nullable=False,
    )

    response_time_ms = Column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="chat_history",
    )