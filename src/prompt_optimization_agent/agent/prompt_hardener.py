"""Prompt hardening agent."""

from pathlib import Path
from typing import Any

from ..core.exceptions import ProviderError
from ..core.utils.logger import logger
from ..interfaces.base_agent import BaseAgent
from ..interfaces.base_provider import BaseProvider


class PromptHardener(BaseAgent):
    """
    Agent responsible for hardening prompts with safety rules, anti-hallucination safeguards, and edge case handling.
    """

    def __init__(self, provider: BaseProvider):
        """
        Initialize the prompt hardener agent.

        Args:
            provider (BaseProvider): The LLM provider to use.
        """
        super().__init__(provider)
        self.prompt_template = ""
        self._load_prompt_template()

    def _load_prompt_template(self) -> None:
        """
        Load the hardener prompt template from the markdown file.

        If file not found, use a default template.
        """
        template_file = Path(__file__).parent / "prompts" / "hardener.md"
        logger.info(f"Loading hardener template from {template_file}")
        if template_file.exists():
            try:
                with template_file.open(encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded hardener template.")
            except OSError as e:
                logger.error(f"Failed to load hardener template: {e}")
                self._set_default_template()
        else:
            logger.warning("Hardener template file not found. Using default.")
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default hardener prompt template."""
        self.prompt_template = """
# Prompt Hardener

Harden the given prompt by adding:
1. Anti-hallucination safeguards
2. Clarification rules
3. Edge case handling
4. Output format enforcement

Return the hardened prompt.
"""

    def run(self, input_data: str) -> dict[str, Any]:
        """
        Harden a prompt by adding safety rules and edge case handling.

        Args:
            input_data (str): The prompt to harden (pass as 'prompt' key in actual usage).

        Returns:
            Dict[str, Any]: Result containing the hardened prompt and metadata.
        """
        logger.info("Starting prompt hardening.")

        prompt_to_harden = input_data
        if isinstance(input_data, dict):
            prompt_to_harden = input_data.get("prompt", "")

        full_prompt = f"Prompt to harden:\n\n{prompt_to_harden}"

        try:
            hardened_prompt = self.provider.generate(full_prompt, system_prompt=self.prompt_template)
            logger.info("Prompt hardening successful.")
            return {
                "hardened_prompt": hardened_prompt.strip(),
                "original_prompt": prompt_to_harden,
            }
        except Exception as e:
            logger.error(f"Prompt hardening failed: {e}")
            if isinstance(e, ProviderError):
                raise
            raise ProviderError(f"Failed to harden prompt: {e}") from e
