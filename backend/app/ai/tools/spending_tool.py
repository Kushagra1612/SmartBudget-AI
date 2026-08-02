from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.repositories.dashboard_repository import DashboardRepository


class SpendingTool(BaseTool):

    name = "spending"

    description = (
        "Returns spending grouped by category."
    )

    def execute(
        self,
        *,
        db: Session,
        user_id,
        month: int,
        year: int,
    ):

        return DashboardRepository.get_category_totals(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )