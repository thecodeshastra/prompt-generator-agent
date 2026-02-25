"""Unit tests for the result exporter."""

import os
import shutil
import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from prompt_optimization_agent.core.utils.exporter import save_result_to_markdown


class TestExporter(unittest.TestCase):
    """Test the exporter utility."""

    def setUp(self):
        self.test_output_dir = "test_output"
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        os.makedirs(self.test_output_dir)

        import prompt_optimization_agent.core.utils.exporter as exporter_module

        self.original_output_dir = exporter_module.OUTPUT_DIR
        exporter_module.OUTPUT_DIR = Path(self.test_output_dir)

    def tearDown(self):
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        import prompt_optimization_agent.core.utils.exporter as exporter_module

        exporter_module.OUTPUT_DIR = self.original_output_dir

    def test_save_result_to_markdown_basic(self):
        """Test basic markdown saving."""
        result = {
            "generated_prompt": "Test Prompt",
            "review": {"approved": True, "rating": 5, "feedback": "Great"},
            "test_cases": [{"input": "i", "expected_output": "o"}],
        }
        user_input = "Tell me a joke"

        path = save_result_to_markdown(result, user_input)

        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            content = f.read()
            self.assertIn("Test Prompt", content)
            self.assertIn("Tell me a joke", content)
            self.assertIn("✅ Yes", content)

    def test_save_result_to_markdown_failure(self):
        """Test saving failure results (should still save if explicitly called)."""
        result = {"error": "Pipeline failed", "generated_prompt": None}
        user_input = "Error case"

        path = save_result_to_markdown(result, user_input)
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            content = f.read()
            self.assertIn("❌ No", content)


if __name__ == "__main__":
    unittest.main()
