from datetime import date
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    date: date
    description: str
    debit: float
    credit: float
    balance: float
    merchant: str
    category: str
    payment_mode: str
    transaction_type: str


class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True