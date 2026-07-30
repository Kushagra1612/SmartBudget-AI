from decimal import Decimal
from datetime import date
from uuid import UUID

from pydantic import BaseModel


class TopCategory(BaseModel):
    category: str
    amount: Decimal


class RecentTransaction(BaseModel):
    id: UUID
    transaction_date: date
    merchant: str
    category: str
    amount: Decimal
    transaction_type: str


class MonthlyTrend(BaseModel):
    month: str
    income: Decimal
    expense: Decimal


class DashboardResponse(BaseModel):
    monthly_income: Decimal
    monthly_expenses: Decimal
    savings: Decimal

    total_transactions: int
    total_budgets: int

    financial_health_score: int

    top_categories: list[TopCategory]

    recent_transactions: list[RecentTransaction]

    monthly_trend: list[MonthlyTrend]