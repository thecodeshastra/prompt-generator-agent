"""Custom exception classes for the prompt generator agent."""

class PromptAgentError(Exception):
    """Base exception for all errors in the prompt generator agent."""
    pass

class ProviderError(PromptAgentError):
    """Raised when an LLM provider fails (e.g., API errors, connection issues)."""
    pass

class ParsingError(PromptAgentError):
    """Raised when parsing of LLM output fails (e.g., malformed JSON)."""
    pass

class ConfigurationError(PromptAgentError):
    """Raised when there is an issue with the application configuration."""
    pass

class OrchestratorError(PromptAgentError):
    """Raised when the orchestrator fails to coordinate the pipeline."""
    pass
