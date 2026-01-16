"""OpenAI SDK provider implementation."""

# standard library imports
from typing import Optional

# decouple
from decouple import config

# openai sdk
from openai import OpenAI

from core.exceptions import ProviderError

# core imports
from core.utils.logger import logger

# interface module
from interfaces.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    """
    Provider implementation using the official OpenAI SDK.
    """

    def __init__(
        self,
        model_name: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """
        Initialize the OpenAI SDK provider.

        Args:
            model_name (str): The name of the model to use.
            api_key (Optional[str]): OpenAI API key.
            base_url (Optional[str]): Custom base URL for OpenAI-compatible APIs.
            temperature (float): The temperature for generation.
            max_tokens (int): The maximum tokens to generate.
        """
        self.model_name = model_name
        self.api_key = api_key or config("OPENAI_API_KEY")
        self.base_url = base_url or config("OPENAI_BASE_URL")
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment or arguments.")
            
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response using the OpenAI SDK.

        Args:
            prompt (str): The user prompt.
            system_prompt (Optional[str]): An optional system prompt.

        Returns:
            str: The generated text.

        Raises:
            ProviderError: If the OpenAI SDK fails.
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise ProviderError(f"OpenAI SDK generation failed: {e}") from e
