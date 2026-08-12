from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

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