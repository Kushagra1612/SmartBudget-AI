from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard_schema import (
    DashboardResponse,
    MonthlyTrend,
    RecentTransaction,
    TopCategory,
)
from app.services.budget_service import BudgetService
from decimal import Decimal


class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ) -> DashboardResponse:

        income = DashboardRepository.get_monthly_income(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        expenses = DashboardRepository.get_monthly_expenses(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        savings = income - expenses

        total_transactions = DashboardRepository.get_total_transactions(
            db=db,
            user_id=user_id,
        )

        total_budgets = DashboardRepository.get_total_budgets(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        budget_summary = BudgetService.get_budget_summary(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        top_categories = [
            TopCategory(
                category=row.category.value if hasattr(row.category, "value") else row.category,
                amount=row.amount,
            )
            for row in DashboardRepository.get_top_categories(
                db=db,
                user_id=user_id,
                month=month,
                year=year,
            )
        ]

        recent_transactions = [
            RecentTransaction(
                id=t.id,
                transaction_date=t.transaction_date,
                merchant=t.merchant,
                category=t.category.value if hasattr(t.category, "value") else t.category,
                amount=t.amount,
                transaction_type=t.transaction_type.value
                if hasattr(t.transaction_type, "value")
                else t.transaction_type,
            )
            for t in DashboardRepository.get_recent_transactions(
                db=db,
                user_id=user_id,
            )
        ]

        # Placeholder until monthly trend is implemented
        monthly_trend: list[MonthlyTrend] = []

        # Simple health score (will improve later with AI)
        health_score = 100

        if expenses > income:
             health_score = 40
        elif expenses > income * Decimal("0.80"):
             health_score = 70
        elif expenses > income * Decimal("0.60"):
             health_score = 85

        return DashboardResponse(
            monthly_income=income,
            monthly_expenses=expenses,
            savings=savings,
            total_transactions=total_transactions,
            total_budgets=total_budgets,
            financial_health_score=health_score,
            top_categories=top_categories,
            recent_transactions=recent_transactions,
            monthly_trend=monthly_trend,
        )