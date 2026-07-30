from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CategorySpending:
    category: str
    amount: Decimal
    percentage: float


@dataclass
class SpendingAnalysis:
    total_expense: Decimal
    transaction_count: int
    average_transaction: Decimal
    top_category: str | None
    categories: list[CategorySpending]


class SpendingAnalysisEngine:

    @staticmethod
    def analyze(
        category_totals: dict[str, Decimal],
    ) -> SpendingAnalysis:
        """
        Analyze spending grouped by category.

        NOTE:
        transaction_count currently represents the number of
        categories because only aggregated category totals are
        available. When the real transaction count becomes
        available, update this calculation accordingly.
        """

        total_expense = sum(
            category_totals.values(),
            Decimal("0"),
        )

        # Currently counts categories, not individual transactions.
        transaction_count = len(category_totals)

        average_transaction = (
            total_expense / Decimal(transaction_count)
            if transaction_count > 0
            else Decimal("0")
        )

        categories: list[CategorySpending] = []

        top_category: str | None = None
        highest_amount = Decimal("0")

        for category, amount in category_totals.items():

            percentage = (
                float((amount / total_expense) * 100)
                if total_expense > 0
                else 0.0
            )

            categories.append(
                CategorySpending(
                    category=category,
                    amount=amount,
                    percentage=round(percentage, 2),
                )
            )

            if amount > highest_amount:
                highest_amount = amount
                top_category = category

        categories.sort(
            key=lambda item: item.amount,
            reverse=True,
        )

        return SpendingAnalysis(
            total_expense=total_expense,
            transaction_count=transaction_count,
            average_transaction=average_transaction.quantize(
                Decimal("0.01")
            )
            if transaction_count > 0
            else Decimal("0.00"),
            top_category=top_category,
            categories=categories,
        )