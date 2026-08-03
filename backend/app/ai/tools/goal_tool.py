from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.services.goal_service import GoalService


class GoalTool(BaseTool):
    """
    Tool for retrieving a user's
    financial goals.
    """

    name = "goal"

    description = (
        "Returns the user's active "
        "financial goals."
    )

    def execute(
        self,
        *,
        db: Session,
        user_id: UUID,
        month: int,
        year: int,
    ):

        goals = GoalService.get_user_goals(
            db=db,
            user_id=user_id,
        )

        result = []

        for goal in goals:

            progress = GoalService.calculate_progress(
                goal,
            )

            result.append(
                {
                    "title": goal.title,
                    "target_amount": goal.target_amount,
                    "current_amount": goal.current_amount,
                    "target_date": goal.target_date,
                    "status": goal.status,
                    "remaining": progress["remaining"],
                    "progress": progress["progress"],
                    "days_left": progress["days_left"],
                    "monthly_required": progress[
                        "monthly_required"
                    ],
                }
            )

        return result