from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StatementResponse(BaseModel):

    id: UUID
    original_filename: str
    bank: str | None
    month: int | None
    year: int | None
    pages: int | None
    confidence: float | None
    uploaded_at: datetime
    transaction_count: int