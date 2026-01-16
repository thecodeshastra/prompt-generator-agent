import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from agent.orchestrator import PromptGeneratorOrchestrator
from agent.prompt_generator import PromptGenerator
from agent.prompt_reviewer import PromptReviewer
from agent.test_case_generator import TestCaseGenerator
from interfaces.base_provider import BaseProvider


class MockProvider(BaseProvider):
    """Mock provider for testing."""

    def __init__(self, response: str):
        self.response = response

    def generate(self, prompt: str, system_prompt=None):
        """Return mock response."""
        return self.response


class TestPromptGenerator(unittest.TestCase):
    """Test the prompt generator agent."""

    def test_generate_without_memory(self):
        """Test prompt generation without memory."""
        provider = MockProvider("Generated prompt text")
        generator = PromptGenerator(provider, use_memory=False)

        result = generator.run("Test input")
        self.assertIn("generated_prompt", result)
        self.assertEqual(result["generated_prompt"], "Generated prompt text")


class TestPromptReviewer(unittest.TestCase):
    """Test the prompt reviewer agent."""

    def test_review_approved(self):
        """Test successful review."""
        mock_response = '{"approved": true, "rating": 5, "feedback": "Excellent"}'
        provider = MockProvider(mock_response)
        reviewer = PromptReviewer(provider)

        result = reviewer.run("Test prompt")
        self.assertTrue(result["approved"])
        self.assertEqual(result["rating"], 5)


class TestTestCaseGenerator(unittest.TestCase):
    """Test the test case generator agent."""

    def test_generate_test_cases(self):
        """Test test case generation."""
        mock_response = '[{"input": "test", "expected_output": "result"}]'
        provider = MockProvider(mock_response)
        test_gen = TestCaseGenerator(provider)

        result = test_gen.run("Test prompt")
        self.assertEqual(len(result["test_cases"]), 1)


class TestOrchestrator(unittest.TestCase):
    """Test the orchestrator pipeline."""

    @patch("agent.orchestrator.get_provider")
    def test_full_pipeline_approved(self, mock_get_provider):
        """Test full pipeline with approval."""
        # Mock responses
        mock_provider = Mock()
        mock_provider.generate.side_effect = [
            "Generated prompt",  # Generator
            '{"approved": true, "rating": 4, "feedback": "Good"}',  # Reviewer
            '[{"input": "test", "expected_output": "result"}]',  # Test generator
        ]
        mock_get_provider.return_value = mock_provider

        orchestrator = PromptGeneratorOrchestrator()
        result = orchestrator.run_pipeline("Test input")

        self.assertIn("generated_prompt", result)
        self.assertTrue(result["review"]["approved"])
        self.assertEqual(len(result["test_cases"]), 1)


if __name__ == "__main__":
    unittest.main()
