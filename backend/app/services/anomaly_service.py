from uuid import UUID

from sqlalchemy.orm import Session

from app.ml.anomaly_detector import MIN_TRANSACTIONS_FOR_DETECTION, detect
from app.models.anomaly import Anomaly
from app.models.transaction import TransactionType
from app.repositories.anomaly_repository import AnomalyRepository
from app.repositories.transaction_repository import TransactionRepository


class AnomalyService:
    """
    Business logic for spending-anomaly detection (Phase 7).

    Re-runs Isolation Forest detection over the user's transactions on
    every call (see app/ml/anomaly_detector.py for why), persists any
    newly-flagged transactions so they have a stable history, and skips
    ones already on record so re-scanning is safe to call repeatedly.
    """

    @staticmethod
    def get_user_anomalies(
        db: Session,
        *,
        user_id: UUID,
    ) -> dict:

        transactions = TransactionRepository.get_by_user_id(
            db=db,
            user_id=user_id,
        )

        expense_count = sum(
            1 for t in transactions if t.transaction_type == TransactionType.EXPENSE
        )

        if expense_count < MIN_TRANSACTIONS_FOR_DETECTION:
            return {
                "anomalies": [],
                "total_transactions_analyzed": expense_count,
                "insufficient_data": True,
                "message": (
                    f"Need at least {MIN_TRANSACTIONS_FOR_DETECTION} expense "
                    f"transactions to detect anomalies -- you have "
                    f"{expense_count} so far."
                ),
            }

        results = detect(transactions)

        already_flagged = AnomalyRepository.get_flagged_transaction_ids(
            db=db,
            user_id=user_id,
        )

        new_anomalies = [
            Anomaly(
                user_id=user_id,
                transaction_id=result.transaction_id,
                amount=result.amount,
                reason=result.reason,
                confidence_score=result.confidence_score,
                detected=True,
            )
            for result in results
            if result.transaction_id not in already_flagged
        ]

        AnomalyRepository.bulk_create(
            db=db,
            anomalies=new_anomalies,
        )

        all_anomalies = AnomalyRepository.get_user_anomalies(
            db=db,
            user_id=user_id,
        )

        return {
            "anomalies": all_anomalies,
            "total_transactions_analyzed": expense_count,
            "insufficient_data": False,
            "message": None,
        }
