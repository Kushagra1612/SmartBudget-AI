from app.ai.financial_agent import FinancialAgent
from app.ai.planner import Planner
from app.ai.tool_executor import ToolExecutor


class AgentOrchestrator:
    """
    Coordinates planning, tool execution,
    and final response generation.
    """

    def __init__(self):

        self.planner = Planner()
        self.executor = ToolExecutor()
        self.agent = FinancialAgent()

    def run(
        self,
        *,
        db,
        user_id,
        month: int,
        year: int,
        question: str,
    ):

        plan = self.planner.plan(question)

        tool_results = self.executor.execute(
            tools=plan.tools,
            db=db,
            user_id=user_id,
            month=month,
            year=year,
        )

        return self.agent.handle_query(
            question=question,
            analytics=tool_results,
        )