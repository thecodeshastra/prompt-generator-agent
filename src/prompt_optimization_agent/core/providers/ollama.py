"""Ollama provider module for AI agent"""

# standard library imports

import requests
from ..exceptions import ProviderError

# decouple
from decouple import config

# interface module
from ...interfaces.base_provider import BaseProvider
from ...config.settings import TIMEOUT_SECONDS


class OllamaProvider(BaseProvider):
    """
    Ollama local LLM provider.

    Args:
        BaseProvider (BaseProvider): Base provider class.
    """

    def __init__(self, model_name: str = "llama3.1:8b", temperature: float = 0.7, timeout: int = None):
        """
        Initialize the Ollama provider.

        Args:
            model_name (str): The name of the model to use.
            temperature (float): The temperature for generation.
            timeout (int): Timeout in seconds (defaults to TIMEOUT_SECONDS from settings).
        """
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout or TIMEOUT_SECONDS
        self.url = config("OLLAMA_API_URL", default="http://localhost:11434/api/generate")

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        Generate a response using the Ollama API.

        Args:
            prompt (str): The user prompt.
            system_prompt (Optional[str]): An optional system prompt.

        Returns:
            str: The generated text.

        Raises:
            ProviderError: If the API call fails.
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
            },
        }

        try:
            response = requests.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            raise ProviderError(f"Ollama generation failed: {e}") from e
