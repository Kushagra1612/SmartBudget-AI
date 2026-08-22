from pydantic import BaseModel, Field


class FinancialAdviceRequest(BaseModel):
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2000)


class FinancialAdviceResponse(BaseModel):
    advice: str
    agents_used: list[str] = []


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    month: int | None = Field(default=None, ge=1, le=12)
    year: int | None = Field(default=None, ge=2000)


class ChatResponse(BaseModel):
    response: str
    agents_used: list[str] = []

class AIPulseResponse(BaseModel):
    message: str
    status: str
    agents_used: list[str] = []