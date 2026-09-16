from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionResponse, TransactionUpdate
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get(
    "",
    response_model=list[TransactionResponse],
)
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    stmt = (
        select(Transaction)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.is_deleted.is_(False),
        )
        .order_by(
            Transaction.transaction_date.desc()
        )
    )

    return db.execute(stmt).scalars().all()


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: UUID,
    update_data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Manually update a transaction's category and/or merchant -- lets
    the user recategorize transactions the automatic matcher couldn't
    identify (most commonly person-to-person transfers).
    """

    try:

        return TransactionService.update_transaction(
            db=db,
            user_id=current_user.id,
            transaction_id=transaction_id,
            update_data=update_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )