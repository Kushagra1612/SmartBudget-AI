import logging

from app.ai.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes tools selected by the planner.

    The executor is responsible for:
    - Running multiple tools
    - Handling tool failures
    - Returning successful results
    """

    def __init__(self):
        self.registry = ToolRegistry()

    def execute(
        self,
        *,
        tools: list[str],
        db,
        user_id,
        month: int,
        year: int,
    ) -> dict:

        results = {}

        for tool_name in tools:

            tool = self.registry.get(tool_name)

            if tool is None:
                logger.warning(
                    "Unknown tool requested: %s",
                    tool_name,
                )
                continue

            try:

                results[tool_name] = tool.execute(
                    db=db,
                    user_id=user_id,
                    month=month,
                    year=year,
                )

            except Exception as exc:

                logger.exception(
                    "Tool '%s' failed.",
                    tool_name,
                )

                results[tool_name] = {
                    "status": "error",
                    "message": str(exc),
                }

        return results