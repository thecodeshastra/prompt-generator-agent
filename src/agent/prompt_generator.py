"""Prompt generator agent."""

import os
from typing import Dict, Any, Optional
from interfaces.base_agent import BaseAgent
from interfaces.base_provider import BaseProvider
from .memory.memory_manager import MemoryManager
from core.utils.logger import logger


class PromptGenerator(BaseAgent):
    """
    Agent responsible for generating prompts based on user input.

    Uses memory for prompt engineering notes if enabled.
    """

    def __init__(self, provider: BaseProvider, use_memory: bool = True):
        """
        Initialize the prompt generator agent.

        Args:
            provider (BaseProvider): The AI provider to use.
            use_memory (bool): Whether to use memory for notes.
        """
        super().__init__(provider)
        self.use_memory = use_memory
        self.memory_manager: Optional[MemoryManager] = None
        self.prompt_template = ""

        if self.use_memory:
            self.memory_manager = MemoryManager()

        self._load_prompt_template()

    def _load_prompt_template(self) -> None:
        """
        Load the prompt template from the markdown file.

        If file not found, use a default template.
        """
        template_file = os.path.join(
            os.path.dirname(__file__), "prompts", "generator.md"
        )
        logger.info(f"Loading prompt generator template from {template_file}")
        if os.path.exists(template_file):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded prompt generator template.")
            except IOError as e:
                logger.error(f"Failed to load generator template: {e}")
                self._set_default_template()
        else:
            logger.warning("Generator template file not found. Using default.")
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default prompt template."""
        self.prompt_template = """
# Prompt Generator

Generate a high-quality prompt based on the user's description.
Make it clear, specific, and actionable.
"""

    def run(self, user_input: str, previous_prompt: Optional[str] = None, feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a prompt based on user input, with optional improvement feedback.

        Args:
            user_input (str): The user's description of the desired prompt.
            previous_prompt (Optional[str]): The previously generated prompt to improve.
            feedback (Optional[str]): Feedback from the reviewer on what to improve.

        Returns:
            Dict[str, Any]: Result containing the generated prompt and metadata.
        """
        logger.info("Starting prompt generation.")

        # Get relevant memory notes
        memory_notes = ""
        if self.memory_manager:
            notes = self.memory_manager.get_relevant_notes(user_input)
            logger.debug(f"Retrieved notes: {type(notes)}, value: {repr(notes)}")
            if notes:
                logger.debug("Processing notes as string")
                memory_notes = "\n\nRelevant Notes:\n" + notes

        # Build the full prompt
        improvement_section = ""
        if previous_prompt and feedback:
            improvement_section = f"\n\nPrevious Prompt:\n{previous_prompt}\n\nFeedback: {feedback}\n\nPlease improve the prompt based on this feedback."

        full_prompt = (
            f"{memory_notes}\n\nUser Request: {user_input}{improvement_section}"
        ).strip()

        # Generate response
        try:
            generated_prompt = self.provider.generate(full_prompt, system_prompt=self.prompt_template)
            logger.info("Prompt generation successful.")
            return {
                "generated_prompt": generated_prompt.strip(),
                "memory_used": bool(memory_notes),
                "notes_count": len(notes) if "notes" in locals() else 0,
                "improved": bool(previous_prompt and feedback),
            }
        except Exception as e:
            logger.error(f"Prompt generation failed: {e}")
            raise
