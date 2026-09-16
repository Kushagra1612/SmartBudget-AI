from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.transaction import (
    Transaction,
    TransactionCategory,
    TransactionType,
)
from app.repositories.anomaly_repository import AnomalyRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionUpdate


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

                # Category strings from merchants.json (via
                # CategoryEngine/FuzzyMatcher) are the SAME strings as
                # TransactionCategory's enum values (e.g. "Food",
                # "Grocery", "Transport") -- no translation table
                # needed. A manually-maintained category_map dict here
                # previously caused several categories (Travel, Bills,
                # Income) to silently fall back to OTHER whenever its
                # keys drifted out of sync with merchants.json or the
                # enum. Direct lookup removes that whole class of bug:
                # any future category just needs to exist in both
                # merchants.json and the enum, nothing else to update.
                try:
                    category = TransactionCategory(
                        tx.get("category", "Other")
                    )
                except ValueError:
                    category = TransactionCategory.OTHER

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
                    description=(tx.get("description") or "")[:500],
                    # This field was previously missing entirely --
                    # CategoryEngine.categorize() always computed
                    # payment_mode on the parsed dict via
                    # PaymentDetector.detect(), but it was never passed
                    # into the Transaction(...) constructor here, so it
                    # was silently dropped before ever reaching the
                    # database (every row was saved with payment_mode
                    # = NULL regardless of what the detector found).
                    payment_mode=tx.get("payment_mode", "OTHER"),
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

    @staticmethod
    def update_transaction(
        db: Session,
        *,
        user_id: UUID,
        transaction_id: UUID,
        update_data: TransactionUpdate,
    ) -> Transaction:
        """
        Apply a manual edit (category and/or merchant) to a single
        transaction. This exists mainly for person-to-person UPI
        transfers, which have no business name for the automatic
        merchant matcher to find -- letting the user manually
        recategorize (e.g. "Rent", "Friend repayment") makes those
        transactions useful instead of permanently stuck as
        Other/Unknown.
        """

        transaction = TransactionRepository.get_by_id(
            db=db,
            transaction_id=transaction_id,
        )

        if transaction is None:
            raise ValueError("Transaction not found.")

        if transaction.user_id != user_id:
            raise ValueError("Transaction not found.")

        changes = update_data.model_dump(exclude_unset=True)

        for key, value in changes.items():
            setattr(transaction, key, value)

        updated_transaction = TransactionRepository.update(
            db=db,
            transaction=transaction,
        )

        # A manual edit means the user has corrected something the
        # automatic categorization got wrong -- any anomaly flag tied
        # to this transaction was potentially based on that wrong
        # categorization, so clear it. If the transaction is still
        # genuinely unusual under its corrected category, the next
        # anomaly scan will naturally re-flag it on its own merits.
        AnomalyRepository.delete_by_transaction_id(
            db=db,
            transaction_id=updated_transaction.id,
        )

        return updated_transaction