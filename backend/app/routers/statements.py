from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.statement_schema import StatementResponse
from app.services.statement_service import StatementService

router = APIRouter(
    prefix="/statements",
    tags=["Statements"],
)


@router.get(
    "",
    response_model=list[StatementResponse],
)
def get_statements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    statements = StatementService.list_user_statements(
        db=db,
        user_id=current_user.id,
    )

    return [
        StatementResponse(
            id=statement.id,
            original_filename=statement.original_filename,
            bank=statement.bank,
            month=statement.month,
            year=statement.year,
            pages=statement.pages,
            confidence=statement.confidence,
            uploaded_at=statement.uploaded_at,
            transaction_count=len(
                TransactionRepository.get_by_statement_id(
                    db=db,
                    statement_id=statement.id,
                )
            ),
        )
        for statement in statements
    ]


@router.delete(
    "/{statement_id}",
)
def delete_statement(
    statement_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    statement = StatementService.get_statement(
        db=db,
        statement_id=statement_id,
    )

    if statement is None:
        raise HTTPException(
            status_code=404,
            detail="Statement not found.",
        )

    if statement.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Statement not found.",
        )

    StatementService.delete_statement(
        db=db,
        statement_id=statement_id,
    )

    return {
        "message": "Statement deleted successfully."
    }