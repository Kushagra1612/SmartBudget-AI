from decimal import Decimal
from dataclasses import dataclass


@dataclass
class FinancialScore:
    score: int
    grade: str
    status: str


class FinancialScoreEngine:

    @staticmethod
    def calculate(
        *,
        income: Decimal,
        expenses: Decimal,
        overspent_categories: int,
    ) -> FinancialScore:

        score = 100

        if income > 0:

            expense_ratio = expenses / income

            if expense_ratio > Decimal("1.0"):
                score -= 40

            elif expense_ratio > Decimal("0.90"):
                score -= 25

            elif expense_ratio > Decimal("0.75"):
                score -= 15

            elif expense_ratio > Decimal("0.60"):
                score -= 5

        score -= overspent_categories * 5

        score = max(0, min(100, score))

        if score >= 90:
            grade = "A+"
            status = "Excellent"

        elif score >= 80:
            grade = "A"
            status = "Very Good"

        elif score >= 70:
            grade = "B"

            status = "Good"

        elif score >= 60:
            grade = "C"

            status = "Average"

        elif score >= 50:
            grade = "D"

            status = "Poor"

        else:
            grade = "F"

            status = "Critical"

        return FinancialScore(
            score=score,
            grade=grade,
            status=status,
        )