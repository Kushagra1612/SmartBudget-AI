from pydantic import BaseModel
from typing import List


class TransactionResponse(BaseModel):
    date: str
    description: str
    debit: float
    credit: float
    balance: float
    merchant: str
    category: str
    payment_mode: str
    transaction_type: str


class UploadResponse(BaseModel):
    filename: str
    transactions_found: int
    message: str
    method: str
    transactions: List[TransactionResponse]