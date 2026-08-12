import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    category = Column(
        String(100),
        nullable=False,
        index=True,
    )

    monthly_limit = Column(
        Numeric(12, 2),
        nullable=False,
    )

    month = Column(
        Integer,
        nullable=False,
        index=True,
    )

    year = Column(
        Integer,
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="budgets",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category",
            "month",
            "year",
            name="uq_budget_user_category_month_year",
        ),
    )