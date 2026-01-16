"""Orchestrator for the prompt generator agent pipeline."""

from typing import Any, Dict, Optional

from config.settings import USE_MEMORY
from core.exceptions import ParsingError, ProviderError
from core.provider_factory import get_provider
from core.utils.logger import logger
from interfaces.base_provider import BaseProvider

from .prompt_generator import PromptGenerator
from .prompt_reviewer import PromptReviewer
from .test_case_generator import TestCaseGenerator


class PromptGeneratorOrchestrator:
    """
    Orchestrates the 3-stage pipeline: Generate → Review → Test Cases (if approved).
    """

    def __init__(self, provider: Optional[BaseProvider] = None):
        """
        Initialize the orchestrator.

        Args:
            provider (Optional[BaseProvider]): Custom provider. If None, uses config.
        """
        self.provider = provider or get_provider()
        self.generator = PromptGenerator(self.provider, USE_MEMORY)
        self.reviewer = PromptReviewer(self.provider)
        self.test_generator = TestCaseGenerator(self.provider)

    def run_pipeline(self, user_input: str, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Run the full pipeline with iterative improvement.

        Args:
            user_input (str): The user's prompt description.
            max_iterations (int): Maximum iterations for refinement loop.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'generated_prompt': The final approved prompt text.
                - 'review': The final review result (Dict).
                - 'test_cases': List of generated test cases (Optional[List]).
                - 'history': Full iteration history (List).
                - 'error': Error message if the pipeline failed (Optional[str]).

        Raises:
            OrchestratorError: If a fatal error occurs during coordination.
        """
        logger.info("Starting prompt generator pipeline.")

        result: Dict[str, Any] = {}
        iteration: int = 0
        previous_prompt: Optional[str] = None
        feedback: Optional[str] = None
        history: list = []

        try:
            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Iteration {iteration}: Generating prompt.")

                # Stage 1: Generate prompt
                gen_result = self.generator.run(user_input, previous_prompt, feedback)
                current_prompt = gen_result["generated_prompt"]
                
                # Ensure we at least have the generated prompt in the result
                result["generated_prompt"] = current_prompt

                # Stage 2: Review prompt
                review_result = self.reviewer.run(current_prompt)
                result["review"] = review_result

                # Record history
                history.append({
                    "iteration": iteration,
                    "generated_prompt": current_prompt,
                    "review": review_result,
                    "generation_metadata": gen_result
                })

                if review_result["approved"]:
                    logger.info(f"Prompt approved after {iteration} iterations.")
                    result["generation_metadata"] = gen_result
                    result["history"] = history

                    # Stage 3: Generate test cases
                    try:
                        test_result = self.test_generator.run(current_prompt)
                        result["test_cases"] = test_result["test_cases"]
                        result["test_metadata"] = test_result
                    except Exception as te:
                        logger.error(f"Test case generation failed: {te}")
                        result["test_cases"] = []
                        result["test_error"] = str(te)
                    break
                else:
                    logger.info(f"Prompt not approved. Feedback: {review_result['feedback']}")
                    previous_prompt = current_prompt
                    feedback = review_result["feedback"]

            if not result.get("review", {}).get("approved", False):
                result["history"] = history
                result["test_cases"] = None
                result["reason"] = f"Prompt not approved after {max_iterations} iterations."

            logger.info("Pipeline completed successfully.")
            return result

        except (ProviderError, ParsingError) as e:
            logger.error(f"Pipeline failed at agent level: {e}")
            result["error"] = str(e)
            result["history"] = history
            return result
        except Exception as e:
            logger.error(f"Pipeline failed with unexpected error: {e}")
            result["error"] = f"Unexpected pipeline error: {e}"
            result["history"] = history
            return result
