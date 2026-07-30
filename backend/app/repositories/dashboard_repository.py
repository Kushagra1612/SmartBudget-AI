from datetime import date
from uuid import UUID

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType


class DashboardRepository:

    @staticmethod
    def get_monthly_income(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ):
        return (
            db.query(
                func.coalesce(func.sum(Transaction.amount), 0)
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.INCOME,
                extract("month", Transaction.transaction_date) == month,
                extract("year", Transaction.transaction_date) == year,
                Transaction.is_deleted.is_(False),
            )
            .scalar()
        )

    @staticmethod
    def get_monthly_expenses(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ):
        return (
            db.query(
                func.coalesce(func.sum(Transaction.amount), 0)
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                extract("month", Transaction.transaction_date) == month,
                extract("year", Transaction.transaction_date) == year,
                Transaction.is_deleted.is_(False),
            )
            .scalar()
        )

    @staticmethod
    def get_total_transactions(
        db: Session,
        *,
        user_id: UUID,
    ):
        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
            )
            .count()
        )

    @staticmethod
    def get_total_budgets(
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
                Budget.is_deleted.is_(False),
            )
            .count()
        )

    @staticmethod
    def get_recent_transactions(
        db: Session,
        *,
        user_id: UUID,
        limit: int = 5,
    ):
        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
            )
            .order_by(
                Transaction.transaction_date.desc(),
                Transaction.created_at.desc(),
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_top_categories(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
        limit: int = 5,
    ):
        return (
            db.query(
                Transaction.category,
                func.sum(Transaction.amount).label("amount"),
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                extract("month", Transaction.transaction_date) == month,
                extract("year", Transaction.transaction_date) == year,
                Transaction.is_deleted.is_(False),
            )
            .group_by(Transaction.category)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
            .all()
        )