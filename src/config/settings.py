"""global settings module for prompt-generator-agent"""

# Standard library imports
import os

# Third-party imports

# Local imports

# Provider settings
# PROVIDER = "litellm" # litellm
# MODEL_NAME = "gemini/gemini-2.5-flash" # for gemini
PROVIDER = "ollama" # for ollama
MODEL_NAME = "llama3.1:8b"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
TIMEOUT_SECONDS = 120
MAX_RETRIES = 3
RETRY_BACKOFF = 2

# LiteLLM specific
LITELLM_MAX_TOKENS = 2048

# Memory settings
USE_MEMORY = True  # Enable memory for prompt generator

# Other
LOG_LEVEL = "INFO"
