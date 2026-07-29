from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BudgetCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=100)
    monthly_limit: Decimal = Field(..., gt=0)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2024)


class BudgetUpdate(BaseModel):
    monthly_limit: Decimal = Field(..., gt=0)


class BudgetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    category: str
    monthly_limit: Decimal
    month: int
    year: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


class BudgetSummary(BaseModel):
    category: str
    monthly_limit: Decimal
    spent: Decimal
    remaining: Decimal
    utilization_percentage: float