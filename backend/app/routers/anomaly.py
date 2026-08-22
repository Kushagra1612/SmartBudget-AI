from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.anomaly_schema import AnomalySummaryResponse
from app.services.anomaly_service import AnomalyService

router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"],
)


@router.get(
    "",
    response_model=AnomalySummaryResponse,
)
def get_anomalies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Re-scan the current user's transactions for unusual spending and
    return every anomaly on record (including ones found on earlier
    scans). Safe to call as often as the frontend likes -- detection
    is cheap at this data scale and never re-flags the same
    transaction twice.
    """

    return AnomalyService.get_user_anomalies(
        db=db,
        user_id=current_user.id,
    )
