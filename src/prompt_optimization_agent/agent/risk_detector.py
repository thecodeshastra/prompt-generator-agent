"""Risk detection agent."""

import json
import re
from pathlib import Path
from typing import Any

from ..core.exceptions import ParsingError, ProviderError
from ..core.utils.logger import logger
from ..interfaces.base_agent import BaseAgent
from ..interfaces.base_provider import BaseProvider


class RiskDetector(BaseAgent):
    """
    Agent responsible for detecting potential risks in prompts including failure points, ambiguity, and hallucination risks.
    """

    def __init__(self, provider: BaseProvider):
        """
        Initialize the risk detector agent.

        Args:
            provider (BaseProvider): The LLM provider to use.
        """
        super().__init__(provider)
        self.prompt_template = ""
        self._load_prompt_template()

    def _load_prompt_template(self) -> None:
        """
        Load the risk detector prompt template from the markdown file.

        If file not found, use a default template.
        """
        template_file = Path(__file__).parent / "prompts" / "risk_detector.md"
        logger.info(f"Loading risk detector template from {template_file}")
        if template_file.exists():
            try:
                with template_file.open(encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded risk detector template.")
            except OSError as e:
                logger.error(f"Failed to load risk detector template: {e}")
                self._set_default_template()
        else:
            logger.warning("Risk detector template file not found. Using default.")
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default risk detector prompt template."""
        self.prompt_template = """
# Risk Detector

Analyze the prompt for potential risks including:
1. Failure points
2. Ambiguity risks
3. Hallucination risks
4. Safety concerns

Return a JSON risk report.
"""

    def run(self, input_data: str) -> dict[str, Any]:
        """
        Detect risks in a prompt.

        Args:
            input_data (str): The prompt to analyze.

        Returns:
            Dict[str, Any]: Risk analysis result.
        """
        logger.info("Starting risk detection.")

        prompt_to_analyze = input_data
        if isinstance(input_data, dict):
            prompt_to_analyze = input_data.get("prompt", "")

        full_prompt = f"Prompt to analyze:\n\n{prompt_to_analyze}"

        try:
            response = self.provider.generate(full_prompt, system_prompt=self.prompt_template)
            logger.info("Risk detection successful.")
        except Exception as e:
            logger.error(f"Risk detection failed: {e}")
            raise ProviderError(f"Failed to detect risks: {e}") from e

        logger.debug(f"Raw risk response: {repr(response)}")

        try:
            risk_result = self._parse_risk_response(response)
            risk_result["original_prompt"] = prompt_to_analyze
            return risk_result
        except Exception as e:
            logger.error(f"Risk response parsing failed: {e}")
            raise ParsingError(f"Failed to parse risk detection response: {e}") from e

    def _parse_risk_response(self, response: str) -> dict[str, Any]:
        """Parse the JSON risk response from the LLM."""
        content = response.strip()

        try:
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1:
                    content = content[start : end + 1]
                else:
                    raise ParsingError("No JSON object found in response.")

            result = json.loads(content)

            return {
                "overall_risk_score": result.get("overall_risk_score", 0),
                "risk_level": result.get("risk_level", "unknown"),
                "risks": result.get("risks", []),
                "summary": result.get("summary", ""),
                "recommendations": result.get("recommendations", []),
            }
        except json.JSONDecodeError as je:
            logger.warning(f"JSON parsing failed, attempting fallback: {je}")

            score_match = re.search(r'"overall_risk_score":\s*(\d+)', response)
            level_match = re.search(r'"risk_level":\s*"(\w+)"', response)

            return {
                "overall_risk_score": int(score_match.group(1)) if score_match else 0,
                "risk_level": level_match.group(1) if level_match else "unknown",
                "risks": [],
                "summary": "Failed to parse detailed risk analysis.",
                "recommendations": [],
            }
