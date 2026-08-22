import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
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
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    statement_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "statements.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================
    # Financial Data
    # ==========================

    amount = Column(
        Numeric(12, 2),
        nullable=False,
    )

    debit = Column(
        Numeric(12, 2),
        nullable=True,
        default=0,
    )

    credit = Column(
        Numeric(12, 2),
        nullable=True,
        default=0,
    )

    balance = Column(
        Numeric(12, 2),
        nullable=True,
    )

    # ==========================
    # Classification
    # ==========================

    transaction_type = Column(
        Enum(TransactionType),
        nullable=False,
    )

    category = Column(
        Enum(TransactionCategory),
        nullable=False,
    )

    payment_mode = Column(
        String(50),
        nullable=True,
    )

    # ==========================
    # Details
    # ==========================

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

    transaction_hash = Column(
        String(64),
        unique=True,
        nullable=True,
        index=True,
    )

    # ==========================
    # Metadata
    # ==========================

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

    # ==========================
    # Relationships
    # ==========================

    user = relationship(
        "User",
        back_populates="transactions",
    )

    statement = relationship(
        "Statement",
        back_populates="transactions",
    )

    anomaly = relationship(
        "Anomaly",
        back_populates="transaction",
        uselist=False,
    )