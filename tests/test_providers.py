"""Unit tests for providers."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.exceptions import ProviderError
from core.providers.ollama import OllamaProvider
from core.providers.openai_sdk import OpenAIProvider


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAIProvider."""

    @patch("core.providers.openai_sdk.OpenAI")
    def test_generate_success(self, mock_openai):
        """Test successful generation."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Success"

        provider = OpenAIProvider(api_key="sk-test")
        result = provider.generate("hello")
        self.assertEqual(result, "Success")

    @patch("core.providers.openai_sdk.OpenAI")
    def test_generate_failure(self, mock_openai):
        """Test generation failure."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        provider = OpenAIProvider(api_key="sk-test")
        with self.assertRaises(ProviderError):
            provider.generate("hello")

class TestOllamaProvider(unittest.TestCase):
    """Test OllamaProvider."""

    @patch("requests.post")
    def test_generate_success(self, mock_post):
        """Test successful generation."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Success"}

        provider = OllamaProvider()
        result = provider.generate("hello")
        self.assertEqual(result, "Success")

    @patch("requests.post")
    def test_generate_failure(self, mock_post):
        """Test generation failure."""
        mock_post.side_effect = Exception("Connection Error")

        provider = OllamaProvider()
        with self.assertRaises(ProviderError):
            provider.generate("hello")

if __name__ == "__main__":
    unittest.main()
