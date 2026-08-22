from uuid import UUID

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.budget_schema import BudgetSummary
from app.services.statement_service import StatementService


class BudgetService:

    @staticmethod
    def create_budget(
        db: Session,
        *,
        user_id: UUID,
        category: str,
        monthly_limit: float,
    ) -> Budget:

        if monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than 0.")

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
        )

        if BudgetRepository.exists(
            db=db,
            user_id=user_id,
            category=category,
            month=month,
            year=year,
        ):
            raise ValueError(
                "Budget already exists for this category and month."
            )

        budget = Budget(
            user_id=user_id,
            category=category.strip(),
            monthly_limit=monthly_limit,
            month=month,
            year=year,
        )

        return BudgetRepository.create(db, budget)

    @staticmethod
    def get_budget(
        db: Session,
        *,
        budget_id: UUID,
    ) -> Budget | None:
        return BudgetRepository.get_by_id(
            db,
            budget_id,
        )

    @staticmethod
    def get_user_budgets(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
    ) -> list[Budget]:

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        return BudgetRepository.get_user_budgets(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

    @staticmethod
    def update_budget(
        db: Session,
        *,
        budget_id: UUID,
        category: str,
        monthly_limit: float,
    ) -> Budget:

        budget = BudgetRepository.get_by_id(
            db=db,
            budget_id=budget_id,
        )

        if budget is None:
            raise ValueError("Budget not found.")

        if monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than 0.")

        existing_budget = BudgetRepository.get_budget(
            db=db,
            user_id=budget.user_id,
            category=category,
            month=budget.month,
            year=budget.year,
        )

        if (
            existing_budget is not None
            and existing_budget.id != budget.id
        ):
            raise ValueError(
                "Budget already exists for this category and month."
            )

        budget.category = category.strip()
        budget.monthly_limit = monthly_limit

        return BudgetRepository.update(
            db,
            budget,
        )

    @staticmethod
    def delete_budget(
        db: Session,
        *,
        budget_id: UUID,
    ) -> None:

        budget = BudgetRepository.get_by_id(
            db=db,
            budget_id=budget_id,
        )

        if budget is None:
            raise ValueError("Budget not found.")

        BudgetRepository.soft_delete(
            db=db,
            budget=budget,
        )

    @staticmethod
    def get_budget_summary(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
    ) -> list[BudgetSummary]:

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        budgets = BudgetRepository.get_user_budgets(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        summary: list[BudgetSummary] = []

        for budget in budgets:

            spent = TransactionRepository.get_category_spending(
                db=db,
                user_id=user_id,
                category=budget.category,
                month=month,
                year=year,
            )

            remaining = budget.monthly_limit - spent

            utilization = (
                float((spent / budget.monthly_limit) * 100)
                if budget.monthly_limit > 0
                else 0
            )

            summary.append(
                BudgetSummary(
                    id=budget.id,
                    category=budget.category.value
                    if hasattr(budget.category, "value")
                    else budget.category,
                    monthly_limit=budget.monthly_limit,
                    spent=spent,
                    remaining=remaining,
                    utilization_percentage=round(utilization, 2),
                )
            )

        return summary