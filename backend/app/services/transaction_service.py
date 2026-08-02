from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.transaction import (
    Transaction,
    TransactionCategory,
    TransactionType,
)
from app.repositories.transaction_repository import TransactionRepository


class TransactionService:

    @staticmethod
    def save_transactions(
        db: Session,
        *,
        user_id,
        statement_id,
        parsed_transactions: list,
    ):

        if not parsed_transactions:
            return []

        transactions: list[Transaction] = []

        category_map = {
            "Food": TransactionCategory.FOOD,
            "Shopping": TransactionCategory.SHOPPING,
            "Transport": TransactionCategory.TRANSPORT,
            "Health": TransactionCategory.HEALTH,
            "Entertainment": TransactionCategory.ENTERTAINMENT,
            "Utilities": TransactionCategory.UTILITIES,
            "Education": TransactionCategory.EDUCATION,
            "Salary": TransactionCategory.SALARY,
            "Investment": TransactionCategory.INVESTMENT,
            "Others": TransactionCategory.OTHER,
            "Other": TransactionCategory.OTHER,
        }

        try:

            for tx in parsed_transactions:

                debit = Decimal(str(tx.get("debit", 0)))
                credit = Decimal(str(tx.get("credit", 0)))
                balance = Decimal(str(tx.get("balance", 0)))

                if debit == 0 and credit == 0:
                    continue

                amount = debit if debit > 0 else credit

                if credit > 0:
                    transaction_type = TransactionType.INCOME
                elif debit > 0:
                    transaction_type = TransactionType.EXPENSE
                else:
                    transaction_type = TransactionType.TRANSFER

                category = category_map.get(
                    tx.get("category", "Other"),
                    TransactionCategory.OTHER,
                )

                transaction = Transaction(
                    user_id=user_id,
                    statement_id=statement_id,
                    amount=amount,
                    debit=debit,
                    credit=credit,
                    balance=balance,
                    transaction_type=transaction_type,
                    category=category,
                    merchant=tx.get("merchant", ""),
                    description=tx.get("description", ""),
                    source="pdf",
                    transaction_date=tx.get("date"),
                )

                transactions.append(transaction)

            if not transactions:
                return []

            return TransactionRepository.bulk_create(
                db=db,
                transactions=transactions,
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save transactions: {str(e)}",
            )