from datetime import date
from decimal import Decimal

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:

    @staticmethod
    def transaction_exists(
        db: Session,
        *,
        user_id,
        transaction_date: date,
        amount: Decimal,
        merchant: str,
        description: str,
    ) -> bool:
        """
        Check whether an identical transaction already exists.
        """

        return (
            db.query(Transaction)
            .filter(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.transaction_date == transaction_date,
                    Transaction.amount == amount,
                    Transaction.merchant == merchant,
                    Transaction.description == description,
                    Transaction.is_deleted.is_(False),
                )
            )
            .first()
            is not None
        )

    @staticmethod
    def bulk_create(
        db: Session,
        transactions: list[Transaction],
    ) -> list[Transaction]:
        """
        Bulk insert transactions while skipping duplicates.
        """

        if not transactions:
            return []

        saved_transactions: list[Transaction] = []

        try:
            for transaction in transactions:

                if TransactionRepository.transaction_exists(
                    db=db,
                    user_id=transaction.user_id,
                    transaction_date=transaction.transaction_date,
                    amount=transaction.amount,
                    merchant=transaction.merchant,
                    description=transaction.description,
                ):
                    continue

                db.add(transaction)
                saved_transactions.append(transaction)

            db.commit()

            for transaction in saved_transactions:
                db.refresh(transaction)

            return saved_transactions

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_by_statement_id(
        db: Session,
        statement_id,
    ) -> list[Transaction]:
        """
        Return all non-deleted transactions belonging to a statement.
        """

        return (
            db.query(Transaction)
            .filter(
                Transaction.statement_id == statement_id,
                Transaction.is_deleted.is_(False),
            )
            .all()
        )

    @staticmethod
    def delete_by_statement_id(
        db: Session,
        statement_id,
    ) -> int:
        """
        Soft delete all transactions belonging to a statement.
        """

        transactions = (
            db.query(Transaction)
            .filter(
                Transaction.statement_id == statement_id,
                Transaction.is_deleted.is_(False),
            )
            .all()
        )

        for transaction in transactions:
            transaction.is_deleted = True

        db.commit()

        return len(transactions)