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


class GoalContribution(BaseModel):
    """
    Request body for adding money toward a goal.

    A separate endpoint (POST /goals/{goal_id}/contribute) uses this
    to INCREMENT current_amount by this amount, rather than requiring
    the frontend to know and resend the goal's current total via
    GoalUpdate.
    """

    amount: Decimal = Field(..., gt=0)


class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str

    target_amount: Decimal
    current_amount: Decimal

    target_date: date

    status: str

    # Computed progress fields (not stored columns) -- populated by
    # GoalService.to_response() using GoalService.calculate_progress().
    # Optional/defaulted so existing construction paths don't break,
    # but every router endpoint should populate these via to_response()
    # so the frontend always has progress info to render.
    remaining: Decimal | None = None
    progress_percentage: float | None = None
    days_left: int | None = None
    monthly_required: Decimal | None = None