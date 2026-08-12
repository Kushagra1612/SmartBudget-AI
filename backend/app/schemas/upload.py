from datetime import date
from typing import List

from pydantic import BaseModel


class TransactionResponse(BaseModel):
    date: date | None
    description: str
    debit: float
    credit: float
    balance: float
    merchant: str
    category: str
    payment_mode: str
    transaction_type: str


class UploadResponse(BaseModel):
    statement_id: str
    filename: str
    bank: str
    pages: int
    confidence: float
    transactions_found: int
    message: str
    method: str
    transactions: List[TransactionResponse]