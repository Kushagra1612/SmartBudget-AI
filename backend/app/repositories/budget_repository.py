from uuid import UUID
from sqlalchemy.orm import Session

from app.models.budget import Budget


class BudgetRepository:

    @staticmethod
    def create(db: Session, budget: Budget) -> Budget:
        db.add(budget)
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def get_by_id(db: Session, budget_id: UUID) -> Budget | None:
        return (
            db.query(Budget)
            .filter(Budget.id == budget_id)
            .first()
        )

    @staticmethod
    def get_budget(
        db: Session,
        *,
        user_id: UUID,
        category: str,
        month: int,
        year: int,
    ) -> Budget | None:
        return (
            db.query(Budget)
            .filter(
                Budget.user_id == user_id,
                Budget.category == category,
                Budget.month == month,
                Budget.year == year,
            )
            .first()
        )

    @staticmethod
    def get_user_budgets(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ):
        return (
            db.query(Budget)
            .filter(
                Budget.user_id == user_id,
                Budget.month == month,
                Budget.year == year,
            )
            .order_by(Budget.category)
            .all()
        )

    @staticmethod
    def update(db: Session, budget: Budget) -> Budget:
        db.commit()
        db.refresh(budget)
        return budget

    @staticmethod
    def soft_delete(db: Session, budget: Budget) -> None:
        db.delete(budget)
        db.commit()

    @staticmethod
    def exists(
        db: Session,
        *,
        user_id: UUID,
        category: str,
        month: int,
        year: int,
    ) -> bool:
        return (
            db.query(Budget)
            .filter(
                Budget.user_id == user_id,
                Budget.category == category,
                Budget.month == month,
                Budget.year == year,
            )
            .first()
            is not None
        )