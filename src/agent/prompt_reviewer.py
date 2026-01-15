"""Prompt reviewer agent."""

import os
from typing import Dict, Any
from interfaces.base_agent import BaseAgent
from interfaces.base_provider import BaseProvider
from core.utils.logger import logger


class PromptReviewer(BaseAgent):
    """
    Agent responsible for reviewing and rating generated prompts.
    """

    def __init__(self, provider: BaseProvider):
        """
        Initialize the prompt reviewer agent.

        Args:
            provider (BaseProvider): The AI provider to use.
        """
        super().__init__(provider)
        self.prompt_template = ""
        self._load_prompt_template()

    def _load_prompt_template(self) -> None:
        """
        Load the reviewer prompt template from the markdown file.

        If file not found, use a default template.
        """
        template_file = os.path.join(
            os.path.dirname(__file__), "prompts", "reviewer.md"
        )
        logger.info(f"Loading prompt reviewer template from {template_file}")
        if os.path.exists(template_file):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded prompt reviewer template.")
            except IOError as e:
                logger.error(f"Failed to load reviewer template: {e}")
                self._set_default_template()
        else:
            logger.warning("Reviewer template file not found. Using default.")
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default reviewer prompt template."""
        self.prompt_template = """
# Prompt Reviewer

Review the generated prompt for clarity, specificity, safety, and effectiveness.
Provide a rating from 1-5 and brief feedback.
Approve if rating >= 4.
Output in JSON format: {"approved": bool, "rating": int, "feedback": str}
"""

    def run(self, generated_prompt: str) -> Dict[str, Any]:
        """
        Review the generated prompt.

        Args:
            generated_prompt (str): The prompt to review.

        Returns:
            Dict[str, Any]: Review result with approval, rating, and feedback.
        """
        logger.info("Starting prompt review.")

        # Build the full prompt
        full_prompt = f"Generated Prompt:\n{generated_prompt}"

        # Generate response
        try:
            response = self.provider.generate(full_prompt, system_prompt=self.prompt_template)
            logger.info("Prompt review successful.")
            logger.debug(f"Raw review response: {repr(response)}")

            # Parse JSON response
            import json
            import re

            content = response.strip()
            
            # 1. Try to extract JSON from markdown code blocks
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # 2. Try to find the first '{' and last '}'
                start = content.find('{')
                end = content.rfind('}')
                if start != -1 and end != -1:
                    content = content[start : end + 1]

            try:
                result = json.loads(content)
                return {
                    "approved": result.get("approved", False),
                    "rating": result.get("rating", 1),
                    "feedback": result.get("feedback", "No feedback provided."),
                }
            except json.JSONDecodeError as je:
                logger.warning(f"JSON validation failed, attempting regex fallback: {je}")
                
                # 3. Last resort: regex extraction of key fields
                rating_match = re.search(r'"rating":\s*(\d+)', response)
                approved_match = re.search(r'"approved":\s*(true|false)', response, re.I)
                feedback_match = re.search(r'"feedback":\s*"([^"]+)"', response)
                
                if rating_match and approved_match:
                    return {
                        "approved": approved_match.group(1).lower() == "true",
                        "rating": int(rating_match.group(1)),
                        "feedback": feedback_match.group(1) if feedback_match else "Extracted from malformed JSON.",
                    }
                raise je

        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Prompt review failed or invalid response: {e}")
            logger.debug(f"Failed response content: {repr(response)}")
            # Fallback: assume not approved
            return {
                "approved": False,
                "rating": 1,
                "feedback": f"Review failed to parse response: {str(e)}",
            }
