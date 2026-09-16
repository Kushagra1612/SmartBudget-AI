from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import (
    TransactionCategory,
    TransactionType,
)


class TransactionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    amount: Decimal

    debit: Decimal | None
    credit: Decimal | None
    balance: Decimal | None

    merchant: str
    description: str | None

    category: TransactionCategory
    transaction_type: TransactionType

    payment_mode: str | None

    transaction_date: date

    created_at: datetime
    updated_at: datetime


class TransactionUpdate(BaseModel):
    """
    Partial update for a transaction -- used so the user can manually
    recategorize/rename a transaction the automatic merchant matcher
    couldn't identify (most commonly person-to-person UPI transfers,
    which have no business name to match against).
    """

    category: TransactionCategory | None = None
    merchant: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )