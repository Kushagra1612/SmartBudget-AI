from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SavingsAnalysis:
    income: Decimal
    expenses: Decimal
    savings: Decimal
    savings_rate: float
    expense_ratio: float
    cash_flow: Decimal
    status: str


class SavingsAnalysisEngine:

    @staticmethod
    def analyze(
        *,
        income: Decimal,
        expenses: Decimal,
    ) -> SavingsAnalysis:

        savings = income - expenses

        savings_rate = (
            float((savings / income) * 100)
            if income > 0
            else 0
        )

        expense_ratio = (
            float((expenses / income) * 100)
            if income > 0
            else 0
        )

        if savings < 0:
            status = "Deficit"

        elif savings_rate >= 30:
            status = "Excellent"

        elif savings_rate >= 20:
            status = "Healthy"

        elif savings_rate >= 10:
            status = "Average"

        else:
            status = "Low Savings"

        return SavingsAnalysis(
            income=income,
            expenses=expenses,
            savings=savings,
            savings_rate=round(savings_rate, 2),
            expense_ratio=round(expense_ratio, 2),
            cash_flow=savings,
            status=status,
        )