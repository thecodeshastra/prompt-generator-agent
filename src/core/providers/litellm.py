"""LiteLLM provider"""

# Standard library imports
from typing import Optional

# Third-party imports
import litellm
import warnings

# Suppress LiteLLM and Pydantic warnings
litellm.suppress_warnings = True
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.main")
warnings.filterwarnings("ignore", message=".*PydanticSerializationUnexpectedValue.*")

# Local imports
from interfaces.base_provider import BaseProvider
from core.utils.logger import logger


class LiteLLMProvider(BaseProvider):
    """Provider using LiteLLM for multi-model support."""

    def __init__(
        self,
        model_name: str,
        temperature: float,
        max_tokens: int,
        timeout: int,
        max_retries: int,
        retry_backoff: float,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response using LiteLLM."""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = litellm.completion(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )
            content = response.choices[0].message.content
            logger.debug(f"Generated content type: {type(content)}, value: {repr(content)}")
            return content.strip()
        except Exception as e:
            logger.error(f"LiteLLM generation failed: {e}")
            raise
