"""Test case generator agent."""

# Standard library imports
import json
import os
from typing import Any, Dict

# Third-party imports
from pypdf import PdfReader

from core.exceptions import ParsingError, ProviderError
from core.utils.logger import logger

# Local imports
from interfaces.base_agent import BaseAgent
from interfaces.base_provider import BaseProvider


class TestCaseGenerator(BaseAgent):
    """
    Agent responsible for generating test cases for validated prompts.
    """

    def __init__(self, provider: BaseProvider):
        """
        Initialize the test case generator agent.

        Args:
            provider (BaseProvider): The LLM provider to use.
        """
        super().__init__(provider)
        self.prompt_template = ""
        self.benchmark_content = ""
        self.benchmark_pdf = os.path.join(os.path.dirname(__file__), "benchmark.pdf")
        self._load_benchmark()
        self._load_prompt_template()

    def _load_benchmark(self) -> None:
        """
        Load benchmark considerations from PDF.

        If PDF not found, log warning.
        """
        if os.path.exists(self.benchmark_pdf):
            try:
                reader = PdfReader(self.benchmark_pdf)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                self.benchmark_content = text.strip()
                logger.info(
                    f"Loaded benchmark from PDF ({len(self.benchmark_content)} chars)."
                )
            except Exception as e:
                logger.error(f"Failed to load benchmark PDF: {e}")
        else:
            logger.warning(f"Benchmark PDF {self.benchmark_pdf} not found.")

    def _load_prompt_template(self) -> None:
        """
        Load the test case generator prompt template from the markdown file.

        If file not found, use a default template.
        """
        template_file = os.path.join(
            os.path.dirname(__file__), "prompts", "test_case_generator.md"
        )
        logger.info(f"Loading test case generator template from {template_file}")
        if os.path.exists(template_file):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    self.prompt_template = f.read().strip()
                logger.info("Loaded test case generator template.")
            except IOError as e:
                logger.error(f"Failed to load test case template: {e}")
                self._set_default_template()
        else:
            logger.warning("Test case template file not found. Using default.")
            self._set_default_template()

    def _set_default_template(self) -> None:
        """Set a default test case generator prompt template."""
        self.prompt_template = """
# Test Case Generator

Generate 3-5 test cases for the given prompt.
Consider benchmark guidelines for quality.
Output as JSON array: [{"input": "example", "expected_output": "result"}]
"""

    def run(self, approved_prompt: str) -> Dict[str, Any]:
        """
        Generate test cases for the approved prompt.

        Args:
            approved_prompt (str): The validated prompt to generate test cases for.

        Returns:
            Dict[str, Any]: Result containing the list of test cases.
        """
        logger.info("Starting test case generation.")

        # Build the full prompt
        if self.benchmark_content:
            system_prompt = f"{self.prompt_template}\n\nBenchmark Guidelines:\n{self.benchmark_content}"
        else:
            system_prompt = self.prompt_template
        full_prompt = f"Approved Prompt:\n{approved_prompt}"

        # Generate response
        try:
            response = self.provider.generate(full_prompt, system_prompt=system_prompt)
            logger.info("Test case generation successful.")
        except Exception as e:
            logger.error(f"Test case generation failed: {e}")
            raise ProviderError(f"Failed to generate test cases from provider: {e}") from e

        import re
        content = response
        try:
            # 1. Try to extract JSON from markdown code blocks
            json_match = re.search(r"```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # 2. Try to find the first '[' or '{' and last ']' or '}'
                start = min((content.find('[') % (len(content) + 1), content.find('{') % (len(content) + 1)))
                end = max(content.rfind(']'), content.rfind('}'))
                if start != len(content) + 1 and end != -1:
                    content = content[start : end + 1]

            try:
                result = json.loads(content)
                
                # Handle cases where the LLM might wrap the array in a dict
                if isinstance(result, dict) and "test_cases" in result:
                    result = result["test_cases"]
                elif isinstance(result, dict):
                    # Try to find any list in the dict
                    for val in result.values():
                        if isinstance(val, list):
                            result = val
                            break
                
                if not isinstance(result, list):
                    raise ParsingError(f"Expected a list of test cases, got {type(result)}")

                return {
                    "test_cases": result[:5],  # Ensure we return at most 5
                    "count": len(result)
                }
            except json.JSONDecodeError as je:
                logger.error(f"TestCase JSON validation failed: {je}")
                raise ParsingError(f"Failed to parse test cases JSON: {je}") from je

        except Exception as e:
            if isinstance(e, ParsingError):
                raise
            logger.error(f"Test case parsing error: {e}")
            raise ParsingError(f"Unexpected error during test case parsing: {e}") from e
