from app.ai.gemini_service import GeminiService
from app.ai.planner import Planner
from app.ai.prompts import (
    CHAT_PROMPT,
    FINANCIAL_ADVICE_PROMPT,
)


class FinancialAgent:

    def __init__(self):
        self.llm = GeminiService()

    def generate_advice(
        self,
        *,
        analytics,
    ) -> str:

        prompt = FINANCIAL_ADVICE_PROMPT.format(
            financial_score=analytics.financial_score.score,
            income=analytics.savings_analysis.income,
            expenses=analytics.savings_analysis.expenses,
            savings=analytics.savings_analysis.savings,
            savings_rate=analytics.savings_analysis.savings_rate,
            expense_ratio=analytics.savings_analysis.expense_ratio,
            budget_utilization=analytics.budget_analysis.overall_utilization,
            overspent_categories=analytics.budget_analysis.overspent_categories,
            top_category=analytics.spending_analysis.top_category,
        )

        return self.llm.generate(prompt)

    def handle_query(
        self,
        *,
        db,
        user_id,
        month: int,
        year: int,
        question: str,
    ) -> str:

        prompt = CHAT_PROMPT.format(
            question=question,
            context=tool_results,
        )

        return self.llm.generate(prompt)