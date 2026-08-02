from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------
# Dashboard Models
# ---------------------------------

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


# ---------------------------------
# Analytics Models
# ---------------------------------

class FinancialScoreResponse(BaseModel):
    score: int
    grade: str
    status: str


class CategorySpendingResponse(BaseModel):
    category: str
    amount: Decimal
    percentage: float


class SpendingAnalysisResponse(BaseModel):
    total_expense: Decimal
    transaction_count: int
    average_transaction: Decimal
    top_category: str | None

    categories: list[CategorySpendingResponse]


class BudgetAnalysisResponse(BaseModel):
    total_budget: Decimal
    total_spent: Decimal
    overall_utilization: float
    overspent_categories: int
    near_limit_categories: int


class SavingsAnalysisResponse(BaseModel):
    income: Decimal
    expenses: Decimal
    savings: Decimal
    savings_rate: float
    expense_ratio: float
    cash_flow: Decimal
    status: str


class AnalyticsResponse(BaseModel):
    financial_score: FinancialScoreResponse
    spending: SpendingAnalysisResponse
    budget: BudgetAnalysisResponse
    savings: SavingsAnalysisResponse


# ---------------------------------
# Dashboard Response
# ---------------------------------

class DashboardResponse(BaseModel):
    monthly_income: Decimal
    monthly_expenses: Decimal
    savings: Decimal

    total_transactions: int
    total_budgets: int

    analytics: AnalyticsResponse

    top_categories: list[TopCategory]

    recent_transactions: list[RecentTransaction]