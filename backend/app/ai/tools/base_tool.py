from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class for every AI tool.
    """

    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs):
        """
        Execute the tool.

        Returns structured data.
        """
        pass