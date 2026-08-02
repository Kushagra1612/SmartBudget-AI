from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.schemas.dashboard_schema import DashboardResponse
from app.services.dashboard_service import DashboardService


class DashboardTool(BaseTool):
    name = "dashboard"

    description = (
        "Returns monthly income, expenses, savings, "
        "analytics, top categories, and recent transactions."
    )

    def execute(
        self,
        *,
        db: Session,
        user_id: UUID,
        month: int,
        year: int,
    ) -> DashboardResponse:

        return DashboardService.get_dashboard(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )