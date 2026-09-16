from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard_schema import (
    AnalyticsResponse,
    BudgetAnalysisResponse,
    CategorySpendingResponse,
    DashboardResponse,
    FinancialScoreResponse,
    RecentTransaction,
    SavingsAnalysisResponse,
    SpendingAnalysisResponse,
    TopCategory,
)
from app.services.analytics_service import AnalyticsService
from app.services.budget_service import BudgetService
from app.services.statement_service import StatementService

class DashboardService:

    @staticmethod
    def _previous_period(month: int, year: int) -> tuple[int, int]:
        """
        Return the (month, year) immediately before the given one,
        rolling over into the previous year when month is January.
        """

        if month == 1:
            return 12, year - 1

        return month - 1, year

    @staticmethod
    def _percentage_change(
        current: "Decimal",
        previous: "Decimal",
    ) -> float | None:
        """
        Percentage change from `previous` to `current`. None when
        `previous` is 0, since the percentage is undefined in that
        case (there's nothing to compare against -- e.g. a brand new
        user with no prior month of data).
        """

        if previous == 0:
            return None

        return round(
            float((current - previous) / previous * 100),
            2,
        )

    @staticmethod
    def get_dashboard(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,   
    ) -> DashboardResponse:

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

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

        # Month-over-month trend -- reuses the same repository methods
        # against the previous month/year, so no new queries needed
        # beyond calling them a second time.
        previous_month, previous_year = DashboardService._previous_period(
            month,
            year,
        )

        previous_income = DashboardRepository.get_monthly_income(
            db=db,
            user_id=user_id,
            month=previous_month,
            year=previous_year,
        )

        previous_expenses = DashboardRepository.get_monthly_expenses(
            db=db,
            user_id=user_id,
            month=previous_month,
            year=previous_year,
        )

        previous_savings = previous_income - previous_expenses

        income_change_percentage = DashboardService._percentage_change(
            income,
            previous_income,
        )

        expenses_change_percentage = DashboardService._percentage_change(
            expenses,
            previous_expenses,
        )

        savings_change_percentage = DashboardService._percentage_change(
            savings,
            previous_savings,
        )

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

        category_totals = DashboardRepository.get_category_totals(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        overspent_categories = sum(
            1
            for budget in budget_summary
            if budget.utilization_percentage >= 100
        )

        analytics = AnalyticsService.generate(
            income=income,
            expenses=expenses,
            overspent_categories=overspent_categories,
            category_totals=category_totals,
            budget_summary=budget_summary,
        )

        top_categories = [
            TopCategory(
                category=(
                    row.category.value
                    if hasattr(row.category, "value")
                    else row.category
                ),
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
                category=(
                    t.category.value
                    if hasattr(t.category, "value")
                    else t.category
                ),
                amount=t.amount,
                transaction_type=(
                    t.transaction_type.value
                    if hasattr(t.transaction_type, "value")
                    else t.transaction_type
                ),
            )
            for t in DashboardRepository.get_recent_transactions(
                db=db,
                user_id=user_id,
            )
        ]

        return DashboardResponse(
            monthly_income=income,
            monthly_expenses=expenses,
            savings=savings,
            total_transactions=total_transactions,
            total_budgets=total_budgets,
            income_change_percentage=income_change_percentage,
            expenses_change_percentage=expenses_change_percentage,
            savings_change_percentage=savings_change_percentage,
            analytics=AnalyticsResponse(
                financial_score=FinancialScoreResponse(
                    score=analytics.financial_score.score,
                    grade=analytics.financial_score.grade,
                    status=analytics.financial_score.status,
                ),
                spending=SpendingAnalysisResponse(
                    total_expense=analytics.spending_analysis.total_expense,
                    transaction_count=analytics.spending_analysis.transaction_count,
                    average_transaction=analytics.spending_analysis.average_transaction,
                    top_category=analytics.spending_analysis.top_category,
                    categories=[
                        CategorySpendingResponse(
                            category=c.category,
                            amount=c.amount,
                            percentage=c.percentage,
                        )
                        for c in analytics.spending_analysis.categories
                    ],
                ),
                budget=BudgetAnalysisResponse(
                    total_budget=analytics.budget_analysis.total_budget,
                    total_spent=analytics.budget_analysis.total_spent,
                    overall_utilization=analytics.budget_analysis.overall_utilization,
                    overspent_categories=analytics.budget_analysis.overspent_categories,
                    near_limit_categories=analytics.budget_analysis.near_limit_categories,
                ),
                savings=SavingsAnalysisResponse(
                    income=analytics.savings_analysis.income,
                    expenses=analytics.savings_analysis.expenses,
                    savings=analytics.savings_analysis.savings,
                    savings_rate=analytics.savings_analysis.savings_rate,
                    expense_ratio=analytics.savings_analysis.expense_ratio,
                    cash_flow=analytics.savings_analysis.cash_flow,
                    status=analytics.savings_analysis.status,
                ),
            ),
            top_categories=top_categories,
            recent_transactions=recent_transactions,
        )