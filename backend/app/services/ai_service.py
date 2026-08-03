from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.context_builder import ContextBuilder
from app.ai.financial_agent import FinancialAgent
from app.ai.planner import Planner
from app.ai.tool_executor import ToolExecutor
from app.repositories.dashboard_repository import DashboardRepository
from app.services.analytics_service import AnalyticsService
from app.services.budget_service import BudgetService


class AIService:
   
    planner = Planner()
    executor = ToolExecutor()
    agent = FinancialAgent()

    @staticmethod
    def _generate_analytics(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ):
       

        income = DashboardRepository.get_monthly_income(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        expenses = DashboardRepository.get_monthly_expenses(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        category_totals = DashboardRepository.get_category_totals(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        budget_summary = BudgetService.get_budget_summary(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        overspent_categories = sum(
            1
            for budget in budget_summary
            if budget.utilization_percentage >= 100
        )

        return AnalyticsService.generate(
            income=income,
            expenses=expenses,
            overspent_categories=overspent_categories,
            category_totals=category_totals,
            budget_summary=budget_summary,
        )

    @staticmethod
    def get_financial_advice(
        db: Session,
        *,
        user_id: UUID,
        month: int,
        year: int,
    ) -> str:
       
        analytics = AIService._generate_analytics(
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        return AIService.agent.generate_advice(
            analytics=analytics,
        )

@staticmethod
def chat(
    db: Session,
    *,
    user_id: UUID,
    month: int,
    year: int,
    question: str,
) -> str:

    try:

        history = AIService.agent.memory.get_recent_history()

        tools = AIService.planner.plan(
            question=question,
            history=history,
        )

    except Exception:

        tools = ["dashboard"]

    tool_results = AIService.executor.execute(
        tools=tools,
        db=db,
        user_id=user_id,
        month=month,
        year=year,
    )

    context = ContextBuilder.build(tool_results)

    if not context.strip():
        context = (
            "No financial information "
            "could be collected."
        )
   
    return AIService.agent.handle_query(
        question=question,
        context=context,
    )