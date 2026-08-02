from app.ai.tools.budget_tool import BudgetTool
from app.ai.tools.dashboard_tool import DashboardTool
from app.ai.tools.spending_tool import SpendingTool


class ToolRegistry:
    """
    Registry containing all tools available
    to the Financial Agent.
    """

    def __init__(self):

        self.tools = {
            DashboardTool.name: DashboardTool(),
            BudgetTool.name: BudgetTool(),
            SpendingTool.name: SpendingTool(),
        }

    def get(self, tool_name: str):
        return self.tools.get(tool_name)

    def list_tools(self):
        return list(self.tools.values())

    def tool_descriptions(self):

        return "\n".join(
            f"- {tool.name}: {tool.description}"
            for tool in self.tools.values()
        )