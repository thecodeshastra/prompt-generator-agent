"""Metadata generation utility."""

from datetime import datetime
from typing import Any

from ..config.input_config import ComplexityLevel, PromptMode


class MetadataGenerator:
    """
    Generates metadata for optimized prompts including version, complexity, and target model information.
    """

    DEFAULT_VERSION = "1.0.0"

    def __init__(self):
        """Initialize the metadata generator."""
        self.created_at = datetime.utcnow()

    def generate(
        self,
        mode: PromptMode | str = PromptMode.GENERAL_LLM,
        complexity: ComplexityLevel | str | None = None,
        target_model: str | None = None,
        original_prompt: str | None = None,
        optimization_iterations: int = 1,
    ) -> dict[str, Any]:
        """
        Generate metadata for an optimized prompt.

        Args:
            mode: The output mode used for optimization
            complexity: The complexity level of the prompt
            target_model: The target AI model
            original_prompt: The original user input
            optimization_iterations: Number of optimization iterations

        Returns:
            Dict containing metadata
        """
        mode_str = mode.value if isinstance(mode, PromptMode) else str(mode)
        complexity_str = (
            complexity.value
            if isinstance(complexity, ComplexityLevel)
            else str(complexity)
            if complexity
            else "auto"
        )

        return {
            "version": self.DEFAULT_VERSION,
            "mode": mode_str,
            "complexity_level": complexity_str,
            "target_model": target_model or "auto-detect",
            "created_at": self.created_at.isoformat() + "Z",
            "optimization_iterations": optimization_iterations,
            "original_prompt_length": len(original_prompt) if original_prompt else 0,
        }

    def update(self, existing_metadata: dict[str, Any], **updates: Any) -> dict[str, Any]:
        """
        Update existing metadata with new values.

        Args:
            existing_metadata: Existing metadata dictionary
            **updates: Fields to update

        Returns:
            Updated metadata dictionary
        """
        metadata = existing_metadata.copy()
        metadata.update(updates)
        metadata["updated_at"] = datetime.utcnow().isoformat() + "Z"
        return metadata

    def add_risk_info(self, metadata: dict[str, Any], risk_score: int, risk_level: str) -> dict[str, Any]:
        """
        Add risk analysis information to metadata.

        Args:
            metadata: Existing metadata
            risk_score: Overall risk score (0-10)
            risk_level: Risk level (low/medium/high)

        Returns:
            Metadata with risk info added
        """
        return metadata | {
            "risk_score": risk_score,
            "risk_level": risk_level,
        }

    def to_summary(self, metadata: dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the metadata.

        Args:
            metadata: The metadata dictionary

        Returns:
            Summary string
        """
        return (
            f"v{metadata.get('version', '1.0.0')} | "
            f"Mode: {metadata.get('mode', 'general_llm')} | "
            f"Complexity: {metadata.get('complexity_level', 'mid')} | "
            f"Target: {metadata.get('target_model', 'auto-detect')}"
        )


def generate_metadata(
    mode: PromptMode | str = PromptMode.GENERAL_LLM,
    complexity: ComplexityLevel | str | None = None,
    target_model: str | None = None,
    original_prompt: str | None = None,
    optimization_iterations: int = 1,
) -> dict[str, Any]:
    """
    Convenience function to generate metadata.

    Args:
        mode: The output mode
        complexity: The complexity level
        target_model: Target AI model
        original_prompt: Original user input
        optimization_iterations: Number of iterations

    Returns:
        Metadata dictionary
    """
    generator = MetadataGenerator()
    return generator.generate(
        mode=mode,
        complexity=complexity,
        target_model=target_model,
        original_prompt=original_prompt,
        optimization_iterations=optimization_iterations,
    )
