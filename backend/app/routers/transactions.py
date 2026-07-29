from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.transaction import Transaction
from app.models.user import User

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get("/")
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.date.desc())
    )

    return db.execute(stmt).scalars().all()