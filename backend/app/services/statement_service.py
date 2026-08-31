from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.statement import Statement
from app.repositories.statement_repository import StatementRepository


class StatementService:

    @staticmethod
    def create_statement(
        db: Session,
        *,
        user_id: UUID,
        filename: str,
        original_filename: str,
        bank: str,
        parser_method: str,
        pages: int,
        confidence: float,
        month: int,
        year: int,
        file_hash: str | None = None,
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
            month=month,
            year=year,
            file_hash=file_hash,
        )

        return StatementRepository.create(
            db=db,
            statement=statement,
        )

    @staticmethod
    def get_by_hash(
        db: Session,
        *,
        user_id: UUID,
        file_hash: str,
    ) -> Statement | None:
        """
        Check whether this user already uploaded a statement with this
        exact file content.
        """

        return StatementRepository.get_by_hash(
            db=db,
            user_id=user_id,
            file_hash=file_hash,
        )

    @staticmethod
    def get_statement(
        db: Session,
        statement_id: UUID,
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
        user_id: UUID,
    ) -> list[Statement]:
        """
        Retrieve all statements uploaded by a user.
        """

        return StatementRepository.get_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def get_latest_statement(
        db: Session,
        user_id: UUID,
    ) -> Statement | None:
        """
        Retrieve the latest uploaded statement.
        """

        return StatementRepository.get_latest_statement(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def delete_statement(
        db: Session,
        statement_id: UUID,
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
        user_id: UUID,
    ) -> int:
        """
        Count total uploaded statements for a user.
        """

        return StatementRepository.count_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def resolve_period(
        db: Session,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
    ) -> tuple[int, int]:
        """
        Single source of truth for "which month/year should we use right
        now" -- shared by Dashboard, Budgets, and the AI agents so they
        can never disagree with each other.

        If the user has uploaded a statement, its month/year always wins
        (this is how Dashboard already behaved), regardless of whatever
        month/year was passed in -- there's no month picker anywhere in
        the app, so nothing should ever override this. Only when there's
        no statement at all do explicit month/year (if given) get used,
        falling back to today's real calendar date as a last resort so a
        brand-new user isn't blocked before their first upload.
        """

        statement = StatementService.get_latest_statement(
            db=db,
            user_id=user_id,
        )

        if statement is not None:
            return statement.month, statement.year

        if month is not None and year is not None:
            return month, year

        today = date.today()
        return today.month, today.year