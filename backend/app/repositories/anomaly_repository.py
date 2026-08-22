from uuid import UUID

from sqlalchemy.orm import Session

from app.models.anomaly import Anomaly


class AnomalyRepository:
    """
    Repository responsible for CRUD operations on detected anomalies.
    """

    @staticmethod
    def get_flagged_transaction_ids(
        db: Session,
        *,
        user_id: UUID,
    ) -> set[UUID]:
        """
        Transaction IDs that already have an anomaly record, so the
        service layer can skip re-inserting them on every re-scan.
        """

        rows = (
            db.query(Anomaly.transaction_id)
            .filter(Anomaly.user_id == user_id)
            .all()
        )

        return {row[0] for row in rows}

    @staticmethod
    def bulk_create(
        db: Session,
        anomalies: list[Anomaly],
    ) -> list[Anomaly]:

        if not anomalies:
            return []

        try:
            for anomaly in anomalies:
                db.add(anomaly)

            db.commit()

            for anomaly in anomalies:
                db.refresh(anomaly)

            return anomalies

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_user_anomalies(
        db: Session,
        *,
        user_id: UUID,
    ) -> list[Anomaly]:

        return (
            db.query(Anomaly)
            .filter(
                Anomaly.user_id == user_id,
                Anomaly.detected.is_(True),
            )
            .order_by(Anomaly.confidence_score.desc())
            .all()
        )
