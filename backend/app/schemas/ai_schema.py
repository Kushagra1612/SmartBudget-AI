from pydantic import BaseModel, Field


class FinancialAdviceRequest(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)


class FinancialAdviceResponse(BaseModel):
    advice: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000)


class ChatResponse(BaseModel):
    response: str

class AIPulseResponse(BaseModel):
    message: str
    status: str