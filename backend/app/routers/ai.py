from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.ai_schema import (
    ChatRequest,
    ChatResponse,
    FinancialAdviceRequest,
    FinancialAdviceResponse,
)
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/advice",
    response_model=FinancialAdviceResponse,
)
def financial_advice(
    request: FinancialAdviceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    advice = AIService.get_financial_advice(
        db=db,
        user_id=current_user.id,
        month=request.month,
        year=request.year,
    )

    return FinancialAdviceResponse(
        advice=advice,
    )


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    response = AIService.chat(
        db=db,
        user_id=current_user.id,
        month=request.month,
        year=request.year,
        question=request.message,
    )

    return ChatResponse(
        response=response,
    )