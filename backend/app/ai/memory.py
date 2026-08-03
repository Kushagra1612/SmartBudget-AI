from collections import deque


class Memory:
    """
    Simple conversational memory for the
    financial agent.

    Stores recent interactions to provide
    context for future questions.
    """

    def __init__(
        self,
        max_history: int = 10,
    ):
        self.history = deque(maxlen=max_history)

    def add(
        self,
        *,
        role: str,
        message: str,
    ):

        self.history.append(
            {
                "role": role,
                "message": message,
            }
        )

    def get_context(self) -> str:

        if not self.history:
            return ""

        context = []

        for item in self.history:

            context.append(
                f"{item['role']}: {item['message']}"
            )

        return "\n".join(context)

    def get_recent_history(
        self,
        limit: int = 4,
    ) -> str:

        history = list(self.history)[-limit:]

        if not history:
            return ""

        return "\n".join(
            f"{item['role']}: {item['message']}"
            for item in history
        )

    def clear(self):

        self.history.clear()