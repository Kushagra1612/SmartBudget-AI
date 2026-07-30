from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BudgetInsight:
    category: str
    budget: Decimal
    spent: Decimal
    remaining: Decimal
    utilization: float
    status: str


@dataclass
class BudgetAnalysis:
    total_budget: Decimal
    total_spent: Decimal
    overall_utilization: float
    overspent_categories: int
    near_limit_categories: int
    insights: list[BudgetInsight]


class BudgetAnalysisEngine:

    @staticmethod
    def analyze(
        budget_summary,
    ) -> BudgetAnalysis:

        total_budget = Decimal("0")
        total_spent = Decimal("0")

        overspent = 0
        near_limit = 0

        insights = []

        for budget in budget_summary:

            total_budget += budget.monthly_limit
            total_spent += budget.spent

            utilization = (
                float(
                    (budget.spent / budget.monthly_limit) * 100
                )
                if budget.monthly_limit > 0
                else 0
            )

            if utilization >= 100:
                status = "Overspent"
                overspent += 1

            elif utilization >= 80:
                status = "Near Limit"
                near_limit += 1

            else:
                status = "Healthy"

            insights.append(
                BudgetInsight(
                    category=budget.category,
                    budget=budget.monthly_limit,
                    spent=budget.spent,
                    remaining=budget.remaining,
                    utilization=round(utilization, 2),
                    status=status,
                )
            )

        overall_utilization = (
            float((total_spent / total_budget) * 100)
            if total_budget > 0
            else 0
        )

        return BudgetAnalysis(
            total_budget=total_budget,
            total_spent=total_spent,
            overall_utilization=round(
                overall_utilization,
                2,
            ),
            overspent_categories=overspent,
            near_limit_categories=near_limit,
            insights=insights,
        )