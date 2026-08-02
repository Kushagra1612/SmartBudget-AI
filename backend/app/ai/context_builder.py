from typing import Any


class ContextBuilder:
    """
    Converts tool outputs into a clean,
    structured prompt for Gemini.
    """

    @staticmethod
    def build(tool_results: dict[str, Any]) -> str:

        sections: list[str] = []

        # -----------------------------
        # Dashboard
        # -----------------------------
        dashboard = tool_results.get("dashboard")

        if dashboard and not isinstance(dashboard, dict):

            analytics = dashboard.analytics

            sections.append(
                f"""
========================
DASHBOARD
========================
Monthly Income: ₹{dashboard.monthly_income}
Monthly Expenses: ₹{dashboard.monthly_expenses}
Savings: ₹{dashboard.savings}

Financial Score:
- Score: {analytics.financial_score.score}
- Grade: {analytics.financial_score.grade}
- Status: {analytics.financial_score.status}

Top Categories:
{', '.join(c.category for c in dashboard.top_categories)}

Recent Transactions:
{len(dashboard.recent_transactions)}
"""
            )

        # -----------------------------
        # Budget
        # -----------------------------
        budget = tool_results.get("budget")

        if budget and not isinstance(budget, dict):

            budget_text = ""

            for item in budget:

                budget_text += (
                    f"""
Category: {item.category}
Budget: ₹{item.monthly_limit}
Spent: ₹{item.spent}
Remaining: ₹{item.remaining}
Utilization: {item.utilization_percentage}%
------------------------
"""
                )

            sections.append(
                f"""
========================
BUDGET
========================
{budget_text}
"""
            )

        # -----------------------------
        # Spending
        # -----------------------------
        spending = tool_results.get("spending")

        if spending and not isinstance(spending, dict):

            spending_text = ""

            for category, amount in spending.items():

                spending_text += (
                    f"{category}: ₹{amount}\n"
                )

            sections.append(
                f"""
========================
SPENDING
========================
{spending_text}
"""
            )

        return "\n".join(sections)