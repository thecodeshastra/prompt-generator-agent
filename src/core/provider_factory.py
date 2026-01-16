"""Provider factory module"""

# Standard library imports

# Third-party imports

# Local imports
from config.settings import (
    LITELLM_MAX_TOKENS,
    MAX_RETRIES,
    MAX_TOKENS,
    MODEL_NAME,
    OPENAI_BASE_URL,
    PROVIDER,
    RETRY_BACKOFF,
    TEMPERATURE,
    TIMEOUT_SECONDS,
)
from core.exceptions import ConfigurationError
from core.providers.litellm import LiteLLMProvider
from core.providers.ollama import OllamaProvider
from core.providers.openai_sdk import OpenAIProvider
from core.utils.logger import logger


def get_provider():
    """Get provider based on configuration.

    Returns:
        BaseProvider: The configured provider instance.

    Raises:
        ValueError: If provider is unknown.
    """
    logger.info(f"Initializing provider: {PROVIDER}")

    if PROVIDER == "litellm":
        return LiteLLMProvider(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=LITELLM_MAX_TOKENS,
            timeout=TIMEOUT_SECONDS,
            max_retries=MAX_RETRIES,
            retry_backoff=RETRY_BACKOFF,
        )
    elif PROVIDER == "ollama":
        return OllamaProvider(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
        )
    elif PROVIDER == "openai":
        return OpenAIProvider(
            model_name=MODEL_NAME,
            base_url=OPENAI_BASE_URL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    else:
        raise ConfigurationError(f"Unknown provider: {PROVIDER}. Supported: 'litellm', 'ollama', 'openai'")
