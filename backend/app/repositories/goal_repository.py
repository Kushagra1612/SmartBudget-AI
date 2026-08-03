from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_goal import UserGoal


class GoalRepository:
    """
    Repository responsible for CRUD operations
    on user financial goals.
    """

    @staticmethod
    def create(
        db: Session,
        goal: UserGoal,
    ) -> UserGoal:

        db.add(goal)
        db.commit()
        db.refresh(goal)

        return goal

    @staticmethod
    def get_by_id(
        db: Session,
        goal_id: UUID,
    ) -> UserGoal | None:

        return (
            db.query(UserGoal)
            .filter(UserGoal.id == goal_id)
            .first()
        )

    @staticmethod
    def get_user_goals(
        db: Session,
        *,
        user_id: UUID,
    ) -> list[UserGoal]:

        return (
            db.query(UserGoal)
            .filter(
                UserGoal.user_id == user_id,
                UserGoal.status == "ACTIVE",
            )
            .order_by(UserGoal.target_date)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        goal: UserGoal,
    ) -> UserGoal:

        db.commit()
        db.refresh(goal)

        return goal

    @staticmethod
    def delete(
        db: Session,
        goal: UserGoal,
    ) -> None:

        db.delete(goal)
        db.commit()