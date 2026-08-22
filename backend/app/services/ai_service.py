from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.graph import financial_graph
from app.ai.memory import Memory
from app.services.statement_service import StatementService


class AIService:
    """
    Public interface is unchanged from before the LangGraph rebuild --
    get_dashboard_pulse / get_financial_advice / chat all take the same
    arguments and return the same shapes. What changed is everything
    underneath: this now runs the request through financial_graph
    (app/ai/graph.py) instead of a hand-rolled planner/executor loop.
    """

    # One Memory per user instead of one shared for the whole process --
    # the old version's AIService.agent was a single class-level
    # FinancialAgent (and therefore a single Memory) that every user's
    # chat went through, so one person's conversation history could
    # leak into another's. Keyed here instead.
    _memories: dict[UUID, Memory] = {}

    @staticmethod
    def _memory_for(user_id: UUID) -> Memory:
        if user_id not in AIService._memories:
            AIService._memories[user_id] = Memory()
        return AIService._memories[user_id]

    @staticmethod
    def get_dashboard_pulse(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
    ):
        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        result = financial_graph.invoke(
            {
                "mode": "pulse",
                "db": db,
                "user_id": user_id,
                "month": month,
                "year": year,
                "question": "",
                "history": "",
            }
        )

        return {
            "message": result["final_response"].split("\n")[0],
            "status": result["status"],
            "agents_used": result["route"],
        }

    @staticmethod
    def get_financial_advice(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
    ) -> dict:

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        result = financial_graph.invoke(
            {
                "mode": "advice",
                "db": db,
                "user_id": user_id,
                "month": month,
                "year": year,
                "question": "",
                "history": "",
            }
        )

        return {
            "advice": result["final_response"],
            "agents_used": result["route"],
        }

    @staticmethod
    def chat(
        db: Session,
        *,
        user_id: UUID,
        month: int | None = None,
        year: int | None = None,
        question: str,
    ) -> dict:

        month, year = StatementService.resolve_period(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        memory = AIService._memory_for(user_id)

        result = financial_graph.invoke(
            {
                "mode": "chat",
                "db": db,
                "user_id": user_id,
                "month": month,
                "year": year,
                "question": question,
                "history": memory.get_recent_history(),
            }
        )

        response = result["final_response"]

        memory.add(role="User", message=question)
        memory.add(role="Assistant", message=response)

        return {
            "response": response,
            "agents_used": result["route"],
        }
