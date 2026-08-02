import json

from app.ai.gemini_service import GeminiService


class Planner:
    """
    Uses Gemini to decide which tools
    are required for answering a user query.
    """

    def __init__(self):
        self.llm = GeminiService()

    def plan(self, question: str) -> list[str]:

        prompt = f"""
You are an AI planner for a Personal Finance Assistant.

Your job is ONLY to decide which tools should be executed.

Available tools:

1. dashboard
- Monthly income
- Monthly expenses
- Savings
- Financial overview

2. budget
- Budget summary
- Budget utilization
- Overspent categories

3. spending
- Spending by category
- Top spending category
- Expense analysis

Rules:
- Return ONLY valid JSON.
- Do NOT explain anything.
- Do NOT use markdown.
- Do NOT include ```json.
- Use one or more tools if needed.

Examples:

Question:
How much did I spend this month?

Output:
{{"tools":["spending"]}}

Question:
Can I afford a new laptop?

Output:
{{"tools":["dashboard","budget","spending"]}}

Question:
How healthy are my finances?

Output:
{{"tools":["dashboard","budget"]}}

User Question:
{question}
"""

        response = self.llm.generate(prompt)

        # Remove markdown if Gemini adds it
        response = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            data = json.loads(response)

            tools = data.get("tools", [])

            if not isinstance(tools, list):
                return ["dashboard"]

            return tools if tools else ["dashboard"]

        except Exception:
            return ["dashboard"]