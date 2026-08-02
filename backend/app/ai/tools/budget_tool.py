from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.services.budget_service import BudgetService


class BudgetTool(BaseTool):

    name = "budget"

    description = (
    "Returns budget summary, utilization and overspending."
     )

    def execute(
        self,
        *,
        db: Session,
        user_id,
        month: int,
        year: int,
    ):

        return BudgetService.get_budget_summary(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )