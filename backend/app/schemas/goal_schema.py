from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GoalCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    target_amount: Decimal = Field(..., gt=0)
    target_date: date


class GoalUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    target_amount: Decimal | None = Field(default=None, gt=0)
    current_amount: Decimal | None = Field(default=None, ge=0)
    target_date: date | None = None
    status: str | None = None


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str

    target_amount: Decimal
    current_amount: Decimal

    target_date: date

    status: str