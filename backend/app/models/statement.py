import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Statement(Base):
    __tablename__ = "statements"

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

    filename = Column(
        String(255),
        nullable=False,
    )

    original_filename = Column(
        String(255),
        nullable=False,
    )

    # SHA-256 of the uploaded file's bytes, used to detect re-uploading
    # the exact same statement twice. Nullable because statements
    # created before this column existed have no PDF left to hash (the
    # file is deleted right after parsing) -- those rows just don't
    # participate in duplicate detection.
    file_hash = Column(
        String(64),
        nullable=True,
    )

    bank = Column(
        String(100),
        nullable=True,
    )

    parser_method = Column(
        String(50),
        nullable=True,
    )

    pages = Column(
        Integer,
        nullable=True,
    )

    confidence = Column(
        Float,
        nullable=True,
    )

    month = Column(
        Integer,
        nullable=False,
    )

    year = Column(
        Integer,
        nullable=False,
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="statements",
    )

    transactions = relationship(
        "Transaction",
        back_populates="statement",
        cascade="all, delete-orphan",
    )