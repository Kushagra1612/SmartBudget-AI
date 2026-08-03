from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_goal import UserGoal
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal_schema import GoalCreate, GoalUpdate


class GoalService:
    """
    Business logic for user financial goals.
    """

    @staticmethod
    def create_goal(
        db: Session,
        *,
        user_id: UUID,
        goal: GoalCreate,
    ) -> UserGoal:

        new_goal = UserGoal(
            user_id=user_id,
            title=goal.title.strip(),
            target_amount=goal.target_amount,
            current_amount=Decimal("0"),
            target_date=goal.target_date,
            status="ACTIVE",
        )

        return GoalRepository.create(
            db=db,
            goal=new_goal,
        )

    @staticmethod
    def get_goal(
        db: Session,
        *,
        user_id: UUID,
        goal_id: UUID,
    ) -> UserGoal | None:

        goal = GoalRepository.get_by_id(
            db=db,
            goal_id=goal_id,
        )

        if goal is None:
            return None

        if goal.user_id != user_id:
            return None

        return goal

    @staticmethod
    def get_user_goals(
        db: Session,
        *,
        user_id: UUID,
    ) -> list[UserGoal]:

        return GoalRepository.get_user_goals(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def update_goal(
        db: Session,
        *,
        user_id: UUID,
        goal_id: UUID,
        goal: GoalUpdate,
    ) -> UserGoal:

        existing = GoalRepository.get_by_id(
            db=db,
            goal_id=goal_id,
        )

        if existing is None:
            raise ValueError("Goal not found.")

        if existing.user_id != user_id:
            raise ValueError("Goal not found.")

        update_data = goal.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(existing, key, value)

        return GoalRepository.update(
            db=db,
            goal=existing,
        )

    @staticmethod
    def delete_goal(
        db: Session,
        *,
        user_id: UUID,
        goal_id: UUID,
    ) -> None:

        goal = GoalRepository.get_by_id(
            db=db,
            goal_id=goal_id,
        )

        if goal is None:
            raise ValueError("Goal not found.")

        if goal.user_id != user_id:
            raise ValueError("Goal not found.")

        GoalRepository.delete(
            db=db,
            goal=goal,
        )

    @staticmethod
    def calculate_progress(
        goal: UserGoal,
    ) -> dict:

        remaining = goal.target_amount - goal.current_amount

        progress = (
            float(
                (goal.current_amount / goal.target_amount) * 100
            )
            if goal.target_amount > 0
            else 0
        )

        days_left = max(
            (goal.target_date - date.today()).days,
            0,
        )

        monthly_required = (
            remaining / Decimal(max(days_left / 30, 1))
            if remaining > 0
            else Decimal("0")
        )

        return {
            "remaining": remaining,
            "progress": round(progress, 2),
            "days_left": days_left,
            "monthly_required": monthly_required.quantize(
                Decimal("0.01")
            ),
        }