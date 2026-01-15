"""Logger utility module"""

# Standard library imports
import logging

# Third-party imports

# Local imports
from config.settings import LOG_LEVEL

# Configure logger
logger = logging.getLogger("prompt-generator-agent")
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

# Create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
