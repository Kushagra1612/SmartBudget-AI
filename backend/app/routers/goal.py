from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.goal_schema import (
    GoalCreate,
    GoalResponse,
    GoalUpdate,
)
from app.services.goal_service import GoalService

router = APIRouter(
    prefix="/goals",
    tags=["Goals"],
)


@router.post(
    "",
    response_model=GoalResponse,
)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return GoalService.create_goal(
        db=db,
        user_id=current_user.id,
        goal=goal,
    )


@router.get(
    "",
    response_model=list[GoalResponse],
)
def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return GoalService.get_user_goals(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{goal_id}",
    response_model=GoalResponse,
)
def get_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    goal = GoalService.get_goal(
        db=db,
        user_id=current_user.id,
        goal_id=goal_id,
    )

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found.",
        )

    return goal


@router.put(
    "/{goal_id}",
    response_model=GoalResponse,
)
def update_goal(
    goal_id: UUID,
    goal: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        return GoalService.update_goal(
            db=db,
            user_id=current_user.id,
            goal_id=goal_id,
            goal=goal,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{goal_id}",
)
def delete_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    try:

        GoalService.delete_goal(
            db=db,
            user_id=current_user.id,
            goal_id=goal_id,
        )

        return {
            "message": "Goal deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )