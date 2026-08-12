from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard_schema import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    month: int | None = Query(
        default=None,
        ge=1,
        le=12,
    ),
    year: int | None = Query(
        default=None,
        ge=2000,
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return DashboardService.get_dashboard(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year,
    )