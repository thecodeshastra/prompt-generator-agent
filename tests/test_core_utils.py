"""Unit tests for new core utilities."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from prompt_optimization_agent.core.config.input_config import (
    InputConfig,
    PromptMode,
    ComplexityLevel,
    parse_input_config,
)
from prompt_optimization_agent.core.utils.complexity_analyzer import ComplexityAnalyzer, analyze_complexity
from prompt_optimization_agent.core.utils.metadata_generator import MetadataGenerator, generate_metadata


class TestInputConfig(unittest.TestCase):
    """Test InputConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = InputConfig("test input")
        self.assertEqual(config.user_input, "test input")
        self.assertEqual(config.mode, PromptMode.GENERAL_LLM)
        self.assertIsNone(config.complexity)

    def test_custom_values(self):
        """Test custom configuration values."""
        config = InputConfig(
            "test", mode=PromptMode.AGENT, complexity=ComplexityLevel.LONG, target_model="gpt-4"
        )
        self.assertEqual(config.mode, PromptMode.AGENT)
        self.assertEqual(config.complexity, ComplexityLevel.LONG)
        self.assertEqual(config.target_model, "gpt-4")

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = InputConfig("test", mode=PromptMode.JSON)
        d = config.to_dict()
        self.assertEqual(d["mode"], "json")
        self.assertEqual(d["user_input"], "test")

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {"user_input": "test", "mode": "agent", "complexity": "short"}
        config = InputConfig.from_dict(data)
        self.assertEqual(config.mode, PromptMode.AGENT)
        self.assertEqual(config.complexity, ComplexityLevel.SHORT)


class TestPromptMode(unittest.TestCase):
    """Test PromptMode enum."""

    def test_all_modes_exist(self):
        """Test all required modes exist."""
        self.assertEqual(PromptMode.GENERAL_LLM.value, "general_llm")
        self.assertEqual(PromptMode.CUSTOM_GPT.value, "custom_gpt")
        self.assertEqual(PromptMode.AGENT.value, "agent")
        self.assertEqual(PromptMode.JSON.value, "json")
        self.assertEqual(PromptMode.ACTION_SCHEMA.value, "action_schema")


class TestComplexityAnalyzer(unittest.TestCase):
    """Test ComplexityAnalyzer class."""

    def test_simple_input(self):
        """Test simple input detection."""
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze("write a simple prompt")
        self.assertEqual(result, ComplexityLevel.VERY_SHORT)

    def test_complex_input(self):
        """Test complex input detection."""
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze(
            "create an enterprise production grade multi-agent system with scalability and robust security compliance"
        )
        self.assertEqual(result, ComplexityLevel.LONG)

    def test_mid_level_input(self):
        """Test mid-level input detection."""
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze(
            "create a detailed comprehensive prompt for data analysis with multiple steps"
        )
        self.assertEqual(result, ComplexityLevel.MID)

    def test_get_description(self):
        """Test complexity description."""
        analyzer = ComplexityAnalyzer()
        desc = analyzer.get_complexity_description(ComplexityLevel.LONG)
        self.assertIn("production-grade", desc)

    def test_analyze_with_details(self):
        """Test detailed analysis."""
        analyzer = ComplexityAnalyzer()
        result = analyzer.analyze_with_details("simple test")
        self.assertIn("level", result)
        self.assertIn("word_count", result)


class TestMetadataGenerator(unittest.TestCase):
    """Test MetadataGenerator class."""

    def test_generate_metadata(self):
        """Test basic metadata generation."""
        metadata = generate_metadata(mode=PromptMode.AGENT, target_model="gpt-4", original_prompt="test")
        self.assertEqual(metadata["version"], "1.0.0")
        self.assertEqual(metadata["mode"], "agent")
        self.assertEqual(metadata["target_model"], "gpt-4")
        self.assertIn("created_at", metadata)

    def test_add_risk_info(self):
        """Test adding risk info to metadata."""
        generator = MetadataGenerator()
        metadata = {"version": "1.0.0"}
        updated = generator.add_risk_info(metadata, 3, "low")
        self.assertEqual(updated["risk_score"], 3)
        self.assertEqual(updated["risk_level"], "low")

    def test_to_summary(self):
        """Test metadata summary."""
        generator = MetadataGenerator()
        metadata = {"version": "1.0.0", "mode": "agent", "complexity_level": "long", "target_model": "gpt-4"}
        summary = generator.to_summary(metadata)
        self.assertIn("v1.0.0", summary)
        self.assertIn("agent", summary)


class TestParseInputConfig(unittest.TestCase):
    """Test parse_input_config function."""

    def test_parse_basic(self):
        """Test basic parsing."""
        config = parse_input_config("test", mode="agent", complexity="long")
        self.assertEqual(config.mode, PromptMode.AGENT)
        self.assertEqual(config.complexity, ComplexityLevel.LONG)


if __name__ == "__main__":
    unittest.main()
