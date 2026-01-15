"""Base provider interface."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Optional

# Third-party imports

# Local imports


class BaseProvider(ABC):
    """
    Abstract base class for AI providers.

    This class defines the interface that all AI providers must implement
    to generate responses from prompts.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the AI provider.

        Args:
            prompt (str): The user prompt to generate a response for.
            system_prompt (Optional[str]): Optional system prompt for context.

        Returns:
            str: The generated response from the AI provider.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass
