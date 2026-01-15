"""Provider factory module"""

# Standard library imports

# Third-party imports

# Local imports
from config.settings import (
    PROVIDER,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    TIMEOUT_SECONDS,
    MAX_RETRIES,
    RETRY_BACKOFF,
    LITELLM_MAX_TOKENS,
)
from core.providers.litellm import LiteLLMProvider
from core.providers.ollama import OllamaProvider
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
    else:
        raise ValueError(f"Only 'litellm' provider is supported. Got: {PROVIDER}")
