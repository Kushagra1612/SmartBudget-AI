from sqlalchemy.orm import Session

from app.models.statement import Statement
from app.repositories.statement_repository import StatementRepository


class StatementService:

    @staticmethod
    def create_statement(
        db: Session,
        *,
        user_id,
        filename: str,
        original_filename: str,
        bank: str,
        parser_method: str,
        pages: int,
        confidence: float,
    ) -> Statement:
        """
        Create and save a bank statement.
        """

        statement = Statement(
            user_id=user_id,
            filename=filename,
            original_filename=original_filename,
            bank=bank,
            parser_method=parser_method,
            pages=pages,
            confidence=confidence,
        )

        return StatementRepository.create(
            db=db,
            statement=statement,
        )

    @staticmethod
    def get_statement(
        db: Session,
        statement_id,
    ) -> Statement | None:
        """
        Retrieve a statement by ID.
        """

        return StatementRepository.get_by_id(
            db=db,
            statement_id=statement_id,
        )

    @staticmethod
    def list_user_statements(
        db: Session,
        user_id,
    ) -> list[Statement]:
        """
        Retrieve all statements uploaded by a user.
        """

        return StatementRepository.get_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def delete_statement(
        db: Session,
        statement_id,
    ) -> bool:
        """
        Delete a statement if it exists.
        """

        statement = StatementRepository.get_by_id(
            db=db,
            statement_id=statement_id,
        )

        if statement is None:
            return False

        StatementRepository.delete(
            db=db,
            statement=statement,
        )

        return True

    @staticmethod
    def count_user_statements(
        db: Session,
        user_id,
    ) -> int:
        """
        Count total uploaded statements for a user.
        """

        return StatementRepository.count_by_user(
            db=db,
            user_id=user_id,
        )