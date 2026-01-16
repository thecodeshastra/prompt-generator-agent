"""global settings module for prompt-generator-agent"""

# Standard library imports

# Third-party imports
from decouple import config

# Local imports

# Provider settings
# PROVIDER = "litellm" # litellm
# MODEL_NAME = "gemini/gemini-2.0-flash" # for gemini
# PROVIDER = "openai" # for official openai sdk
# MODEL_NAME = "gpt-4o"
PROVIDER = config("PROVIDER", default="ollama") # for ollama
MODEL_NAME = config("MODEL_NAME", default="llama3.1:8b")
OPENAI_BASE_URL = config("OPENAI_BASE_URL", default="") # Optional for compatibility
TEMPERATURE = config("TEMPERATURE", default=0.7, cast=float)
MAX_TOKENS = config("MAX_TOKENS", default=1000, cast=int)
TIMEOUT_SECONDS = config("TIMEOUT_SECONDS", default=120, cast=int)
MAX_RETRIES = config("MAX_RETRIES", default=3, cast=int)
RETRY_BACKOFF = config("RETRY_BACKOFF", default=2, cast=int)

# LiteLLM specific
LITELLM_MAX_TOKENS = config("LITELLM_MAX_TOKENS", default=2048, cast=int)

# Memory settings
USE_MEMORY = config("USE_MEMORY", default=True, cast=bool)  # Enable memory for prompt generator

# Other
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
