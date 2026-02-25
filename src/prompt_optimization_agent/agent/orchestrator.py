"""Orchestrator for the prompt optimization agent pipeline."""

from collections.abc import Callable
from typing import Any

from ..config.settings import USE_MEMORY
from ..core.config.input_config import PromptMode
from ..core.exceptions import ParsingError, ProviderError
from ..core.provider_factory import get_provider
from ..core.utils.logger import logger
from ..core.utils.metadata_generator import MetadataGenerator
from ..interfaces.base_provider import BaseProvider
from .prompt_generator import PromptOptimizer
from .prompt_hardener import PromptHardener
from .prompt_reviewer import PromptReviewer
from .risk_detector import RiskDetector
from .test_case_generator import TestCaseGenerator


class PromptOptimizationOrchestrator:
    """
    Orchestrates the pipeline:
    Generate → Review → Improve → Risk Detection → Hardening → Test Cases → Metadata.
    """

    def __init__(self, provider: BaseProvider | None = None, mode: PromptMode = PromptMode.GENERAL_LLM):
        """
        Initialize the orchestrator.

        Args:
            provider (Optional[BaseProvider]): Custom provider. If None, uses config.
            mode (PromptMode): The output mode for prompt optimization.
        """
        self.provider = provider or get_provider()
        self.mode = mode
        self.optimizer = PromptOptimizer(self.provider, USE_MEMORY, mode)
        self.reviewer = PromptReviewer(self.provider)
        self.hardener = PromptHardener(self.provider)
        self.risk_detector = RiskDetector(self.provider)
        self.test_generator = TestCaseGenerator(self.provider)
        self.metadata_generator = MetadataGenerator()

    def run_pipeline(
        self,
        user_input: str,
        max_iterations: int = 3,
        mode: PromptMode | None = None,
        output_format: str = "markdown",
        status_callback: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """
        Run the full pipeline with iterative improvement.

        Args:
            user_input (str): The user's prompt description.
            max_iterations (int): Maximum iterations for refinement loop.
            mode (PromptMode): Output mode (general_llm, custom_gpt, agent, json, action_schema).
            output_format (str): Output format - "markdown" or "json".
            status_callback (Optional[Callable[[str], None]]): Optional callback for status updates.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'generated_prompt': The final approved prompt text.
                - 'hardened_prompt': The hardened version (if hardening enabled).
                - 'review': The final review result (Dict).
                - 'risk_analysis': Risk detection results (Dict).
                - 'test_cases': List of generated test cases (Optional[List]).
                - 'metadata': Prompt metadata (Dict).
                - 'history': Full iteration history (List).
                - 'error': Error message if the pipeline failed (Optional[str]).

        Raises:
            OrchestratorError: If a fatal error occurs during coordination.
        """
        if mode:
            self.mode = mode
            self.optimizer.set_mode(mode)

        logger.info(f"Starting prompt optimization pipeline (mode: {self.mode.value}).")
        if status_callback:
            status_callback(f"Starting prompt optimization pipeline (mode: {self.mode.value})...")

        result: dict[str, Any] = {}
        iteration: int = 0
        previous_prompt: str | None = None
        feedback: str | None = None
        history: list = []

        try:
            while iteration < max_iterations:
                iteration += 1
                msg = f"Iteration {iteration}: Optimizing prompt..."
                logger.info(msg)
                if status_callback:
                    status_callback(msg)

                gen_result = self.optimizer.run(user_input, previous_prompt, feedback)
                current_prompt = gen_result["generated_prompt"]

                result["generated_prompt"] = current_prompt

                msg = f"Iteration {iteration}: Reviewing prompt..."
                logger.info(msg)
                if status_callback:
                    status_callback(msg)

                review_result = self.reviewer.run(current_prompt)
                result["review"] = review_result

                history.append(
                    {
                        "iteration": iteration,
                        "generated_prompt": current_prompt,
                        "review": review_result,
                        "generation_metadata": gen_result,
                    }
                )

                if review_result["approved"]:
                    msg = f"Prompt approved after {iteration} iterations."
                    logger.info(msg)
                    if status_callback:
                        status_callback(msg)

                    result["generation_metadata"] = gen_result
                    result["history"] = history

                    # Skip risk detection and hardening for general_llm mode (faster)
                    enable_risk_detection = self.mode not in (PromptMode.GENERAL_LLM,)
                    enable_hardening = self.mode not in (
                        PromptMode.GENERAL_LLM,
                        PromptMode.JSON,
                        PromptMode.ACTION_SCHEMA,
                    )

                    # Use current_prompt for test cases (hardened if available, else current)
                    prompt_for_tests = current_prompt

                    if enable_risk_detection:
                        msg = "Analyzing risks..."
                        logger.info(msg)
                        if status_callback:
                            status_callback(msg)

                        try:
                            risk_result = self.risk_detector.run(current_prompt)
                            result["risk_analysis"] = risk_result
                        except Exception as re:
                            logger.error(f"Risk detection failed: {re}")
                            result["risk_analysis"] = {"error": str(re)}
                    else:
                        result["risk_analysis"] = {
                            "skipped": True,
                            "reason": "Not required for general_llm mode",
                        }

                    if enable_hardening:
                        msg = "Hardening prompt..."
                        logger.info(msg)
                        if status_callback:
                            status_callback(msg)

                        try:
                            hardener_result = self.hardener.run(current_prompt)
                            result["hardened_prompt"] = hardener_result["hardened_prompt"]
                            prompt_for_tests = hardener_result["hardened_prompt"]
                        except Exception as he:
                            logger.error(f"Hardening failed: {he}")
                            result["hardened_prompt"] = current_prompt
                    else:
                        result["hardened_prompt"] = current_prompt

                    msg = "Generating test cases..."
                    logger.info(msg)
                    if status_callback:
                        status_callback(msg)

                    try:
                        test_result = self.test_generator.run(prompt_for_tests)
                        result["test_cases"] = test_result["test_cases"]
                        result["test_metadata"] = test_result
                    except Exception as te:
                        logger.error(f"Test case generation failed: {te}")
                        result["test_cases"] = []
                        result["test_error"] = str(te)

                    metadata = self.metadata_generator.generate(
                        mode=self.mode,
                        target_model=None,
                        original_prompt=user_input,
                        optimization_iterations=iteration,
                    )

                    if (
                        enable_risk_detection
                        and "risk_analysis" in result
                        and "overall_risk_score" in result["risk_analysis"]
                    ):
                        metadata = self.metadata_generator.add_risk_info(
                            metadata,
                            result["risk_analysis"].get("overall_risk_score", 0),
                            result["risk_analysis"].get("risk_level", "unknown"),
                        )

                    result["metadata"] = metadata
                    break
                else:
                    msg = "Prompt not approved. Feedback provided. Refining..."
                    logger.info(msg)
                    if status_callback:
                        status_callback(msg)

                    previous_prompt = current_prompt
                    feedback = review_result["feedback"]

            if not result.get("review", {}).get("approved", False):
                result["history"] = history
                result["test_cases"] = None
                result["reason"] = f"Prompt not approved after {max_iterations} iterations."

            logger.info("Pipeline completed successfully.")
            if status_callback:
                status_callback("Pipeline completed successfully.")
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
