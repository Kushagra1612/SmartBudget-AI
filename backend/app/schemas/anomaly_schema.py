from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnomalyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    transaction_id: UUID

    amount: Decimal
    reason: str
    confidence_score: Decimal
    detected: bool

    created_at: datetime


class AnomalySummaryResponse(BaseModel):
    anomalies: list[AnomalyResponse]
    total_transactions_analyzed: int
    insufficient_data: bool
    message: str | None = None
