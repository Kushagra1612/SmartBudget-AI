import json
import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.context_builder import ContextBuilder
from app.ai.gemini_service import GeminiService
from app.ai.prompts import CHAT_PROMPT, FINANCIAL_ADVICE_PROMPT
from app.ai.tools.budget_tool import BudgetTool
from app.ai.tools.dashboard_tool import DashboardTool
from app.ai.tools.goal_tool import GoalTool
from app.ai.tools.spending_tool import SpendingTool
from app.services.analytics_service import AnalyticsService

ALL_AGENTS = ["dashboard", "budget", "spending", "goal"]

_TOOLS = {
    "dashboard": DashboardTool(),
    "budget": BudgetTool(),
    "spending": SpendingTool(),
    "goal": GoalTool(),
}

_ROUTER_PROMPT = """
You are an AI planner for a Personal Finance Assistant.

Your job is ONLY to decide which specialist agents should run.

Available agents:

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
- Use one or more agents if needed.

Examples:

Question:
How much did I spend this month?

Output:
{{"agents":["spending"]}}

Question:
Can I afford a new laptop?

Output:
{{"agents":["dashboard","budget","spending"]}}

Question:
How healthy are my finances?

Output:
{{"agents":["dashboard","budget"]}}

Question:
Can I buy an iPhone?

Output:
{{"agents":["dashboard","goal"]}}

Question:
How much should I save every month to buy a bike?

Output:
{{"agents":["goal"]}}

Question:
Am I on track to reach my savings goal?

Output:
{{"agents":["goal"]}}

Question:
Will buying a new phone affect my savings goal?

Output:
{{"agents":["dashboard","goal"]}}

Question:
How much money do I have left after expenses?

Output:
{{"agents":["dashboard"]}}

Question:
Where am I spending the most?

Output:
{{"agents":["spending"]}}

Question:
Which budget category is overspent?

Output:
{{"agents":["budget"]}}

Conversation History:
{history}

Current Question:
{question}
"""


class AgentState(TypedDict):
    mode: str  # "pulse" | "advice" | "chat"
    db: Any  # SQLAlchemy Session -- not serializable state in the usual
             # LangGraph sense, but this graph only ever runs in-process
             # via .invoke(), never across a checkpoint boundary, so
             # carrying it through state is safe here.
    user_id: Any
    month: int
    year: int
    question: str
    history: str
    route: list[str]
    agent_outputs: Annotated[dict[str, Any], operator.or_]
    final_response: str
    status: str


def coordinator_node(state: AgentState) -> dict:
    """
    Decides which specialist agents run. For chat, asks Gemini (the same
    prompt/logic the old Planner used). For pulse/advice, always wants
    the full picture, so there's no decision to make -- routes directly.
    """

    if state["mode"] != "chat":
        return {"route": ["dashboard", "budget", "spending"]}

    llm = GeminiService()

    prompt = _ROUTER_PROMPT.format(
        history=state.get("history", ""),
        question=state["question"],
    )

    raw = llm.generate(prompt)
    cleaned = raw.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(cleaned)
        agents = data.get("agents", [])

        if not isinstance(agents, list):
            agents = []

        agents = [a for a in agents if a in ALL_AGENTS]

    except Exception:
        agents = []

    return {"route": agents or ["dashboard"]}


def _make_agent_node(agent_name: str):
    """Builds a node function for one specialist agent."""

    def node(state: AgentState) -> dict:

        tool = _TOOLS[agent_name]

        try:
            result = tool.execute(
                db=state["db"],
                user_id=state["user_id"],
                month=state["month"],
                year=state["year"],
            )
        except Exception as exc:
            result = {"status": "error", "message": str(exc)}

        return {"agent_outputs": {agent_name: result}}

    return node


def _route_to_agents(state: AgentState) -> list[str]:
    """Conditional edge: fan out only to the agents the coordinator picked."""

    return [f"{name}_agent" for name in state["route"]]


def _build_advice_analytics(agent_outputs: dict[str, Any]):
    """
    Reassembles the same analytics object FINANCIAL_ADVICE_PROMPT
    expects, from data the agents already fetched -- no separate direct
    DB calls duplicating what dashboard_agent/budget_agent/spending_agent
    just did.
    """

    dashboard = agent_outputs.get("dashboard")
    budget_summary = agent_outputs.get("budget", [])
    category_totals = agent_outputs.get("spending", {})

    income = dashboard.monthly_income if dashboard else 0
    expenses = dashboard.monthly_expenses if dashboard else 0

    overspent_categories = sum(
        1
        for b in budget_summary
        if getattr(b, "utilization_percentage", 0) >= 100
    )

    return AnalyticsService.generate(
        income=income,
        expenses=expenses,
        overspent_categories=overspent_categories,
        category_totals=category_totals,
        budget_summary=budget_summary,
    )


def responder_node(state: AgentState) -> dict:
    """
    Synthesizes the final answer. Uses FINANCIAL_ADVICE_PROMPT for
    pulse/advice (same structured analytics as before) and CHAT_PROMPT
    for chat (same context+memory+question shape as before) -- the
    prompts themselves are unchanged, only how they get their inputs.
    """

    llm = GeminiService()
    agent_outputs = state.get("agent_outputs", {})

    if state["mode"] in ("pulse", "advice"):

        analytics = _build_advice_analytics(agent_outputs)

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

        response = llm.generate(prompt)

        return {
            "final_response": response,
            "status": analytics.financial_score.status,
        }

    # mode == "chat"
    context = ContextBuilder.build(agent_outputs)

    if not context.strip():
        context = "No financial information could be collected."

    prompt = CHAT_PROMPT.format(
        memory=state.get("history", ""),
        context=context,
        question=state["question"],
    )

    response = llm.generate(prompt)

    return {"final_response": response}


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("coordinator", coordinator_node)

    for agent_name in ALL_AGENTS:
        graph.add_node(f"{agent_name}_agent", _make_agent_node(agent_name))
        graph.add_edge(f"{agent_name}_agent", "responder")

    graph.add_node("responder", responder_node)

    graph.add_edge(START, "coordinator")
    graph.add_conditional_edges(
        "coordinator",
        _route_to_agents,
        path_map=[f"{name}_agent" for name in ALL_AGENTS],
    )
    graph.add_edge("responder", END)

    return graph.compile()


# Compiled once, reused for every request -- compiling is the
# expensive, static part (building the graph structure); running it
# per-request via .invoke() is cheap and holds no state between calls.
financial_graph = build_graph()
