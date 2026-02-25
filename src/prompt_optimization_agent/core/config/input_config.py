"""Input configuration module for prompt optimization."""

from enum import Enum
from typing import Any


class PromptMode(str, Enum):
    """Supported output modes for prompt optimization."""

    GENERAL_LLM = "general_llm"
    CUSTOM_GPT = "custom_gpt"
    AGENT = "agent"
    JSON = "json"
    ACTION_SCHEMA = "action_schema"


class ComplexityLevel(str, Enum):
    """Prompt complexity levels."""

    VERY_SHORT = "very_short"
    SHORT = "short"
    MID = "mid"
    LONG = "long"


class InputConfig:
    """
    Configuration for prompt optimization input.

    Supports both natural language intent and structured configuration.
    """

    def __init__(
        self,
        user_input: str,
        mode: PromptMode | None = None,
        complexity: ComplexityLevel | None = None,
        target_model: str | None = None,
        custom_config: dict[str, Any] | None = None,
    ):
        """
        Initialize input configuration.

        Args:
            user_input: Natural language description of the prompt to optimize
            mode: Output mode (general_llm, custom_gpt, agent, json, action_schema)
            complexity: Desired complexity level (auto-detected if None)
            target_model: Target AI model (e.g., gpt-4, claude-3)
            custom_config: Additional custom configuration
        """
        self.user_input = user_input
        self.mode = mode or PromptMode.GENERAL_LLM
        self.complexity = complexity
        self.target_model = target_model
        self.custom_config = custom_config or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "user_input": self.user_input,
            "mode": self.mode.value,
            "complexity": self.complexity.value if self.complexity else None,
            "target_model": self.target_model,
            "custom_config": self.custom_config,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InputConfig":
        """Create configuration from dictionary."""
        return cls(
            user_input=data.get("user_input", ""),
            mode=PromptMode(data["mode"]) if data.get("mode") else None,
            complexity=ComplexityLevel(data["complexity"]) if data.get("complexity") else None,
            target_model=data.get("target_model"),
            custom_config=data.get("custom_config", {}),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "InputConfig":
        """Create configuration from JSON string."""
        import json

        return cls.from_dict(json.loads(json_str))


def parse_input_config(
    user_input: str,
    mode: str | None = None,
    complexity: str | None = None,
    target_model: str | None = None,
    **kwargs,
) -> InputConfig:
    """
    Parse input arguments into InputConfig.

    Args:
        user_input: Natural language description
        mode: Output mode string
        complexity: Complexity level string
        target_model: Target model string
        **kwargs: Additional configuration

    Returns:
        InputConfig instance
    """
    prompt_mode = PromptMode(mode) if mode else None
    complexity_level = ComplexityLevel(complexity) if complexity else None

    return InputConfig(
        user_input=user_input,
        mode=prompt_mode,
        complexity=complexity_level,
        target_model=target_model,
        custom_config=kwargs,
    )
