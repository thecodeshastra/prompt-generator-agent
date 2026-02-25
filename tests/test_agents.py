import os
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from prompt_optimization_agent.agent.orchestrator import PromptOptimizationOrchestrator
from prompt_optimization_agent.agent.prompt_generator import PromptOptimizer
from prompt_optimization_agent.agent.prompt_hardener import PromptHardener
from prompt_optimization_agent.agent.prompt_reviewer import PromptReviewer
from prompt_optimization_agent.agent.risk_detector import RiskDetector
from prompt_optimization_agent.agent.test_case_generator import TestCaseGenerator
from prompt_optimization_agent.core.config.input_config import PromptMode
from prompt_optimization_agent.interfaces.base_provider import BaseProvider


class MockProvider(BaseProvider):
    """Mock provider for testing."""

    def __init__(self, response: str):
        self.response = response

    def generate(self, prompt: str, system_prompt=None):
        return self.response


class TestPromptOptimizer(unittest.TestCase):
    """Test the prompt optimizer agent."""

    def test_optimize_without_memory(self):
        """Test prompt optimization without memory."""
        provider = MockProvider("Optimized prompt text")
        optimizer = PromptOptimizer(provider, use_memory=False)

        result = optimizer.run("Test input")
        self.assertIn("generated_prompt", result)
        self.assertEqual(result["generated_prompt"], "Optimized prompt text")

    def test_optimize_with_mode(self):
        """Test prompt optimization with custom mode."""
        provider = MockProvider("Optimized prompt")
        optimizer = PromptOptimizer(provider, use_memory=False, mode=PromptMode.AGENT)

        result = optimizer.run("Test input")
        self.assertIn("generated_prompt", result)
        self.assertEqual(result["mode"], "agent")


class TestPromptHardener(unittest.TestCase):
    """Test the prompt hardener agent."""

    def test_harden_prompt(self):
        """Test prompt hardening."""
        mock_response = "Hardened prompt with safeguards"
        provider = MockProvider(mock_response)
        hardener = PromptHardener(provider)

        result = hardener.run("Test prompt")
        self.assertIn("hardened_prompt", result)
        self.assertEqual(result["hardened_prompt"], "Hardened prompt with safeguards")


class TestRiskDetector(unittest.TestCase):
    """Test the risk detector agent."""

    def test_detect_risks(self):
        """Test risk detection."""
        mock_response = '{"overall_risk_score": 3, "risk_level": "low", "risks": [], "summary": "Low risk", "recommendations": []}'
        provider = MockProvider(mock_response)
        detector = RiskDetector(provider)

        result = detector.run("Test prompt")
        self.assertIn("overall_risk_score", result)
        self.assertEqual(result["overall_risk_score"], 3)
        self.assertEqual(result["risk_level"], "low")


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

    @patch("prompt_optimization_agent.agent.orchestrator.get_provider")
    def test_full_pipeline_approved(self, mock_get_provider):
        """Test full pipeline with general_llm mode (skips risk/hardening for speed)."""
        mock_provider = Mock()
        # general_llm mode: Optimize → Review → Test Cases (no risk/hardening)
        mock_provider.generate.side_effect = [
            "Optimized prompt",
            '{"approved": true, "rating": 4, "feedback": "Good"}',
            '[{"input": "test", "expected_output": "result"}]',
        ]
        mock_get_provider.return_value = mock_provider

        orchestrator = PromptOptimizationOrchestrator()
        result = orchestrator.run_pipeline("Test input")

        self.assertIn("generated_prompt", result)
        self.assertTrue(result["review"]["approved"])
        self.assertIn("hardened_prompt", result)
        self.assertIn("risk_analysis", result)
        self.assertTrue(result["risk_analysis"].get("skipped"))  # general_llm skips risk
        self.assertIn("metadata", result)
        self.assertEqual(len(result["test_cases"]), 1)

    @patch("prompt_optimization_agent.agent.orchestrator.get_provider")
    def test_pipeline_with_mode(self, mock_get_provider):
        """Test pipeline with agent mode (includes risk detection and hardening)."""
        mock_provider = Mock()
        # agent mode: Optimize → Review → Risk → Harden → Test Cases
        mock_provider.generate.side_effect = [
            "Optimized prompt",
            '{"approved": true, "rating": 4, "feedback": "Good"}',
            '{"overall_risk_score": 2, "risk_level": "low", "risks": [], "summary": "OK", "recommendations": []}',
            "Hardened prompt",
            '[{"input": "test", "expected_output": "result"}]',
        ]
        mock_get_provider.return_value = mock_provider

        orchestrator = PromptOptimizationOrchestrator(mode=PromptMode.AGENT)
        result = orchestrator.run_pipeline("Test input", mode=PromptMode.AGENT)

        self.assertIn("generated_prompt", result)
        self.assertEqual(result["metadata"]["mode"], "agent")
        self.assertFalse(result["risk_analysis"].get("skipped"))  # agent mode includes risk


if __name__ == "__main__":
    unittest.main()
