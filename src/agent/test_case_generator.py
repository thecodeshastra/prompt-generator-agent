"""Test case generator agent."""

# Standard library imports
import os
import json
from typing import Dict, Any

# Third-party imports
from pypdf import PdfReader

# Local imports
from interfaces.base_agent import BaseAgent
from interfaces.base_provider import BaseProvider
from core.utils.logger import logger


class TestCaseGenerator(BaseAgent):
    """
    Agent responsible for generating test cases for validated prompts.
    """

    def __init__(self, provider: BaseProvider, benchmark_pdf: str = "benchmark.pdf"):
        """
        Initialize the test case generator agent.

        Args:
            provider (BaseProvider): The AI provider to use.
            benchmark_pdf (str): Path to the benchmark PDF file.
        """
        super().__init__(provider)
        self.prompt_template = ""
        self.benchmark_content = ""
        self.benchmark_pdf = os.path.join(os.path.dirname(__file__), benchmark_pdf)
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
        system_prompt = f"{self.prompt_template}\n\nBenchmark Guidelines:\n{self.benchmark_content}" if self.benchmark_content else self.prompt_template
        full_prompt = f"Approved Prompt:\n{approved_prompt}"

        # Generate response
        try:
            response = self.provider.generate(full_prompt, system_prompt=system_prompt)
            logger.info("Test case generation successful.")
            logger.debug(f"Raw test case response: {repr(response)}")

            # Parse JSON response
            import re
            content = response.strip()

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

            test_cases = json.loads(content)
            
            # Ensure it's a list (some models might wrap a single test case in an object)
            if isinstance(test_cases, dict):
                # Look for a list inside the dict
                for key, val in test_cases.items():
                    if isinstance(val, list):
                        test_cases = val
                        break
                else:
                    test_cases = [test_cases]

            if not isinstance(test_cases, list):
                raise ValueError("Response is not a list of test cases.")

            return {
                "test_cases": test_cases,
                "count": len(test_cases),
            }
        except (json.JSONDecodeError, ValueError, Exception) as e:
            logger.error(f"Test case generation failed or invalid response: {e}")
            logger.debug(f"Failed response content: {repr(response)}")
            # Fallback: empty list
            return {
                "test_cases": [],
                "count": 0,
                "error": str(e),
            }
