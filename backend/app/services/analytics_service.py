from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.analytics.budget_analysis import (
    BudgetAnalysis,
    BudgetAnalysisEngine,
)
from app.analytics.financial_score import (
    FinancialScore,
    FinancialScoreEngine,
)
from app.analytics.savings_analysis import (
    SavingsAnalysis,
    SavingsAnalysisEngine,
)
from app.analytics.spending_analysis import (
    SpendingAnalysis,
    SpendingAnalysisEngine,
)


@dataclass
class AnalyticsResult:
    financial_score: FinancialScore
    spending_analysis: SpendingAnalysis
    budget_analysis: BudgetAnalysis
    savings_analysis: SavingsAnalysis


class AnalyticsService:
    @staticmethod
    def generate(
        *,
        income: Decimal,
        expenses: Decimal,
        overspent_categories: int,
        category_totals: dict[str, Decimal],
        budget_summary: list[Any],
    ) -> AnalyticsResult:
        """
        Runs all analytics engines and returns a single AnalyticsResult.
        """

        # Spending Analysis
        spending = SpendingAnalysisEngine.analyze(
            category_totals=category_totals,
        )

        # Financial Score
        financial = FinancialScoreEngine.calculate(
            income=income,
            expenses=expenses,
            overspent_categories=overspent_categories,
        )

        # Budget Analysis
        budget = BudgetAnalysisEngine.analyze(
            budget_summary=budget_summary,
        )

        # Savings Analysis
        savings = SavingsAnalysisEngine.analyze(
            income=income,
            expenses=expenses,
        )

        return AnalyticsResult(
            financial_score=financial,
            spending_analysis=spending,
            budget_analysis=budget,
            savings_analysis=savings,
        )