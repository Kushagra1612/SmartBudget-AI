import json

from app.ai.gemini_service import GeminiService


class Planner:
    """
    Uses Gemini to decide which tools
    are required for answering a user query.
    """

    def __init__(self):
        self.llm = GeminiService()
        
    def plan(
    self,
    question: str,
    history: str = "",
    ) -> list[str]:

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

4. goal
- User financial goals
- Savings targets
- Goal progress
- Goal deadline

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

Question:
Can I buy an iPhone?

Output:
{{"tools":["dashboard","goal"]}}

Question:
How much should I save every month to buy a bike?

Output:
{{"tools":["goal"]}}

Question:
Am I on track to reach my savings goal?

Output:
{{"tools":["goal"]}}

Question:
Will buying a new phone affect my savings goal?

Output:
{{"tools":["dashboard","goal"]}}

Question:
How much money do I have left after expenses?

Output:
{{"tools":["dashboard"]}}

Question:
Where am I spending the most?

Output:
{{"tools":["spending"]}}

Question:
Which budget category is overspent?

Output:
{{"tools":["budget"]}}

Conversation History:

User:
Can I buy a laptop?

Assistant:
Buying a laptop now may delay your savings goal.

Current Question:
What about next month?

Output:
{{"tools":["dashboard","goal"]}}

Conversation History:

User:
Where am I spending the most?

Assistant:
Your highest spending category is Food.

Current Question:
How can I reduce it?

Output:
{{"tools":["spending"]}}

Conversation History:

User:
How is my budget?

Assistant:
Your Food budget is close to its limit.

Current Question:
Should I increase it?

Output:
{{"tools":["budget"]}}


Conversation History:
{history}

Current Question:
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