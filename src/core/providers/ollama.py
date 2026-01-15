"""Ollama provider module for AI agent"""

# standard library imports
import requests
from typing import Optional

# interface module
from interfaces.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    """
    Ollama local LLM provider.

    Args:
        BaseProvider (BaseProvider): Base provider class.
    """

    def __init__(self, model_name: str, temperature: float = 0.2):
        """
        Initialize the Ollama provider.

        Args:
            model_name (str): The model name.
            temperature (float, optional): The temperature. Defaults to 0.2.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using the Ollama provider.

        Args:
            prompt (str): The input prompt.
            system_prompt (str): The system prompt.

        Returns:
            str: The generated response.
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

        response = requests.post(self.url, json=payload)
        response.raise_for_status()

        return response.json()["response"].strip()
