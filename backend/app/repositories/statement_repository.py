from sqlalchemy.orm import Session

from app.models.statement import Statement


class StatementRepository:

    @staticmethod
    def create(
        db: Session,
        statement: Statement,
    ) -> Statement:
        """
        Create a new bank statement.
        """

        db.add(statement)
        db.commit()
        db.refresh(statement)

        return statement

    @staticmethod
    def get_by_id(
        db: Session,
        statement_id,
    ) -> Statement | None:
        """
        Get a statement by its ID.
        """

        return (
            db.query(Statement)
            .filter(
                Statement.id == statement_id,
            )
            .first()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id,
    ) -> list[Statement]:
        """
        Get all statements uploaded by a user.
        """

        return (
            db.query(Statement)
            .filter(
                Statement.user_id == user_id,
            )
            .order_by(
                Statement.uploaded_at.desc(),
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        statement: Statement,
    ) -> None:
        """
        Delete a statement.
        Transactions are automatically deleted because of
        ON DELETE CASCADE.
        """

        db.delete(statement)
        db.commit()

    @staticmethod
    def count_by_user(
        db: Session,
        user_id,
    ) -> int:
        """
        Count uploaded statements for a user.
        """

        return (
            db.query(Statement)
            .filter(
                Statement.user_id == user_id,
            )
            .count()
        )