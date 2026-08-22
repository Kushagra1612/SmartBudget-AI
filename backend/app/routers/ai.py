from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.ai_schema import (
    ChatRequest,
    ChatResponse,
    FinancialAdviceRequest,
    FinancialAdviceResponse,
    AIPulseResponse,
)

from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get(
    "/pulse",
    response_model=AIPulseResponse,
)
def get_ai_pulse(
    month: Optional[int] = Query(default=None),
    year: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return AIService.get_dashboard_pulse(
        db=db,
        user_id=current_user.id,
        month=month,
        year=year,
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

    result = AIService.get_financial_advice(
        db=db,
        user_id=current_user.id,
        month=request.month,
        year=request.year,
    )

    return FinancialAdviceResponse(
        advice=result["advice"],
        agents_used=result["agents_used"],
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

    result = AIService.chat(
        db=db,
        user_id=current_user.id,
        month=request.month,
        year=request.year,
        question=request.message,
    )

    return ChatResponse(
        response=result["response"],
        agents_used=result["agents_used"],
    )