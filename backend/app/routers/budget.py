from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.budget_schema import (
    BudgetCreate,
    BudgetResponse,
    BudgetSummary,
    BudgetUpdate,
)
from app.services.budget_service import BudgetService

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"],
)


@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_budget(
    request: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return BudgetService.create_budget(
            db=db,
            user_id=current_user.id,
            category=request.category,
            monthly_limit=request.monthly_limit,
            month=request.month,
            year=request.year,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[BudgetResponse],
)
def get_budgets(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BudgetService.get_user_budgets(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year,
    )


# IMPORTANT:
# Keep this route ABOVE "/{budget_id}"
@router.get(
    "/summary",
    response_model=list[BudgetSummary],
)
def get_budget_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BudgetService.get_budget_summary(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year,
    )


@router.get(
    "/{budget_id}",
    response_model=BudgetResponse,
)
def get_budget(
    budget_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = BudgetService.get_budget(
        db=db,
        budget_id=budget_id,
    )

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found.",
        )

    if budget.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    return budget


@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
)
def update_budget(
    budget_id: UUID,
    request: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = BudgetService.get_budget(
        db=db,
        budget_id=budget_id,
    )

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found.",
        )

    if budget.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    try:
        return BudgetService.update_budget(
            db=db,
            budget_id=budget_id,
            category=request.category,
            monthly_limit=request.monthly_limit,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_200_OK,
)
def delete_budget(
    budget_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    budget = BudgetService.get_budget(
        db=db,
        budget_id=budget_id,
    )

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found.",
        )

    if budget.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized.",
        )

    BudgetService.delete_budget(
        db=db,
        budget_id=budget_id,
    )

    return {
        "message": "Budget deleted successfully."
    }