"""Base agent interface"""

# Standard library imports
from abc import ABC, abstractmethod

# Third-party imports

# Local imports
from interfaces.base_provider import BaseProvider


class BaseAgent(ABC):
    """Abstract base class for agents."""

    def __init__(self, provider: BaseProvider):
        self.provider = provider

    @abstractmethod
    def run(self, input_data: str) -> dict:
        """
        Run the agent with input data.

        Args:
            input_data (str): The input to process.

        Returns:
            dict: The result of the agent's operation.
        """
        pass
