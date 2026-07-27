import enum
import uuid

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class TransactionType(str, enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"


class TransactionCategory(str, enum.Enum):
    FOOD = "Food"
    SHOPPING = "Shopping"
    TRANSPORT = "Transport"
    HEALTH = "Health"
    ENTERTAINMENT = "Entertainment"
    UTILITIES = "Utilities"
    EDUCATION = "Education"
    SALARY = "Salary"
    INVESTMENT = "Investment"
    OTHER = "Other"


class Transaction(Base):
    __tablename__ = "transactions"

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

    amount = Column(
        Numeric(12, 2),
        nullable=False,
    )

    transaction_type = Column(
        Enum(TransactionType),
        nullable=False,
    )

    category = Column(
        Enum(TransactionCategory),
        nullable=False,
    )

    merchant = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        String(500),
        nullable=True,
    )

    source = Column(
        String(50),
        nullable=False,
        default="manual",
    )

    transaction_date = Column(
        Date,
        nullable=False,
        index=True,
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
        "User",
        back_populates="transactions",
    )