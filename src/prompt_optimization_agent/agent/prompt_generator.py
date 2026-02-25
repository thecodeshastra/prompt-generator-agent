"""Prompt optimization agent."""

from pathlib import Path
from typing import Any

from ..core.config.input_config import PromptMode
from ..core.exceptions import ProviderError
from ..core.utils.logger import logger
from ..interfaces.base_agent import BaseAgent
from ..interfaces.base_provider import BaseProvider
from .memory.memory_manager import MemoryManager


class PromptOptimizer(BaseAgent):
    """
    Agent responsible for optimizing prompts based on user input.

    Uses memory for prompt engineering notes if enabled.
    Supports multiple output modes: general_llm, custom_gpt, agent, json, action_schema.
    """

    def __init__(
        self,
        provider: BaseProvider,
        use_memory: bool = True,
        mode: PromptMode = PromptMode.GENERAL_LLM,
    ):
        """
        Initialize the prompt optimizer agent.

        Args:
            provider (BaseProvider): The LLM provider to use.
            use_memory (bool): Whether to use the memory manager for contextual notes.
            mode (PromptMode): The output mode for prompt optimization.
        """
        super().__init__(provider)
        self.use_memory = use_memory
        self.mode = mode
        self.memory_manager = MemoryManager() if use_memory else None
        self._load_prompt_template()

    def _load_prompt_template(self) -> None:
        """
        Load the prompt template based on the selected mode.

        - general_llm & custom_gpt: Use generator.md (merged template)
        - other modes: Use {mode}.md specific template
        """
        prompts_dir = Path(__file__).parent / "prompts"

        if self.mode in (PromptMode.GENERAL_LLM, PromptMode.CUSTOM_GPT):
            template_file = prompts_dir / "generator.md"
        else:
            template_file = prompts_dir / f"{self.mode.value}.md"

        logger.info(f"Loading prompt template for mode: {self.mode.value}")
        logger.debug(f"Template path: {template_file}")

        if template_file.exists():
            try:
                with template_file.open(encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info(f"Loaded template for mode: {self.mode.value}")
            except OSError as e:
                logger.error(f"Failed to load mode template: {e}")
                self._load_generator_template()
        else:
            logger.warning(f"Mode template {template_file} not found. Using generator.md as fallback.")
            self._load_generator_template()

    def _load_generator_template(self) -> None:
        """Load the original generator template as fallback."""
        template_file = Path(__file__).parent / "prompts" / "generator.md"
        logger.info(f"Loading fallback template from {template_file}")
        if template_file.exists():
            try:
                with template_file.open(encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded fallback template.")
            except OSError as e:
                logger.error(f"Failed to load fallback template: {e}")
                self._set_default_template()
        else:
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default prompt template."""
        self.prompt_template = """
# Prompt Optimizer

Optimize a high-quality prompt based on the user's description.
Make it clear, specific, and actionable.
"""

    def set_mode(self, mode: PromptMode) -> None:
        """
        Change the output mode and reload template.

        Args:
            mode (PromptMode): The new output mode.
        """
        self.mode = mode
        self._load_prompt_template()

    def run(
        self,
        user_input: str,
        previous_prompt: str | None = None,
        feedback: str | None = None,
    ) -> dict[str, Any]:
        """
        Optimize a prompt based on user input, with optional improvement feedback.

        Args:
            user_input (str): The user's description of the desired prompt.
            previous_prompt (Optional[str]): The previously generated prompt to improve.
            feedback (Optional[str]): Feedback from the reviewer on what to improve.

        Returns:
            Dict[str, Any]: Result containing the optimized prompt and metadata.
        """
        logger.info(f"Starting prompt optimization (mode: {self.mode.value}).")

        relevant_notes = ""
        if self.memory_manager:
            notes = self.memory_manager.get_relevant_notes(user_input)
            logger.debug(f"Retrieved notes: {type(notes)}, value: {repr(notes)}")
            if notes:
                logger.debug("Processing notes as string")
                relevant_notes = "\n\nRelevant Notes:\n" + notes

        improvement_section = ""
        if previous_prompt and feedback:
            p_prompt = f"\n\nPrevious Prompt:\n{previous_prompt}\n\n"
            f_prompt = "Feedback: {feedback}\n\nPlease improve the prompt based on this feedback."
            improvement_section = f"{p_prompt}{f_prompt}"

        mode_instruction = self._get_mode_instruction()

        full_prompt = (
            f"{relevant_notes}\n\n{mode_instruction}\n\nUser Request: {user_input}{improvement_section}"
        ).strip()

        try:
            optimized_prompt = self.provider.generate(full_prompt, system_prompt=self.prompt_template)
            logger.info("Prompt optimization successful.")
            return {
                "generated_prompt": optimized_prompt.strip(),
                "mode": self.mode.value,
                "memory_used": bool(relevant_notes),
                "notes_count": len(relevant_notes.split("\n\n")) if relevant_notes else 0,
                "improved": bool(previous_prompt and feedback),
            }
        except Exception as e:
            logger.error(f"Prompt optimization failed: {e}")
            if isinstance(e, ProviderError):
                raise
            raise ProviderError(f"Failed to optimize prompt: {e}") from e

    def _get_mode_instruction(self) -> str:
        """Get mode-specific instruction for the prompt."""
        instructions = {
            PromptMode.GENERAL_LLM: "Optimize this prompt for general LLM use (ChatGPT, Claude, etc.).",
            PromptMode.CUSTOM_GPT: "Optimize this prompt for a Custom GPT (GPT Builder configuration).",
            PromptMode.AGENT: "Optimize this prompt for an AI agent with autonomous capabilities.",
            PromptMode.JSON: "Optimize this prompt to produce structured JSON output for API/automation.",
            PromptMode.ACTION_SCHEMA: "Generate an OpenAPI 3.1.0 schema for AI tool-calling/actions.",
        }
        return instructions.get(self.mode, instructions[PromptMode.GENERAL_LLM])
