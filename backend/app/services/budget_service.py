from uuid import UUID

from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.budget_schema import BudgetSummary


class BudgetService:

    @staticmethod
    def create_budget(
        db: Session,
        *,
        user_id: UUID,
        category: str,
        monthly_limit: float,
        month: int,
        year: int,
    ) -> Budget:

        if monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than 0.")

        if BudgetRepository.exists(
            db,
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
        return BudgetRepository.get_by_id(db, budget_id)

    @staticmethod
    def get_user_budgets(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ) -> list[Budget]:
        return BudgetRepository.get_user_budgets(
            db,
            user_id=user_id,
            month=month,
            year=year,
        )

    @staticmethod
    def update_budget(
        db: Session,
        *,
        budget_id: UUID,
        monthly_limit: float,
    ) -> Budget:

        budget = BudgetRepository.get_by_id(db, budget_id)

        if budget is None:
            raise ValueError("Budget not found.")

        if monthly_limit <= 0:
            raise ValueError("Monthly limit must be greater than 0.")

        budget.monthly_limit = monthly_limit

        return BudgetRepository.update(db, budget)

    @staticmethod
    def delete_budget(
        db: Session,
        *,
        budget_id: UUID,
    ) -> None:

        budget = BudgetRepository.get_by_id(db, budget_id)

        if budget is None:
            raise ValueError("Budget not found.")

        BudgetRepository.soft_delete(db, budget)

    @staticmethod
    def get_budget_summary(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ) -> list[BudgetSummary]:

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