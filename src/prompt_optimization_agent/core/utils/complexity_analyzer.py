"""Complexity analyzer for automatic prompt complexity detection."""

import re
from typing import Any

from ..config.input_config import ComplexityLevel


class ComplexityAnalyzer:
    """
    Analyzes user input to determine appropriate prompt complexity level.

    Automatically selects between very_short, short, mid, and long.
    """

    COMPLEXITY_KEYWORDS = {
        ComplexityLevel.VERY_SHORT: [
            "simple",
            "quick",
            "brief",
            "one sentence",
            "minimal",
        ],
        ComplexityLevel.SHORT: [
            "short",
            "basic",
            "simple task",
            "straightforward",
        ],
        ComplexityLevel.MID: [
            "detailed",
            "comprehensive",
            "thorough",
            "complete",
            "multi-step",
            "workflow",
            "process",
        ],
        ComplexityLevel.LONG: [
            "enterprise",
            "production",
            "complex",
            "advanced",
            "full system",
            "detailed guide",
            "comprehensive framework",
            "multi-agent",
            "scalable",
            "robust",
        ],
    }

    COMPLEXITY_INDICATORS = {
        ComplexityLevel.VERY_SHORT: 50,
        ComplexityLevel.SHORT: 150,
        ComplexityLevel.MID: 300,
        ComplexityLevel.LONG: 500,
    }

    def __init__(self):
        """Initialize the complexity analyzer."""
        self._keyword_weights = {
            ComplexityLevel.VERY_SHORT: 1.0,
            ComplexityLevel.SHORT: 1.5,
            ComplexityLevel.MID: 2.0,
            ComplexityLevel.LONG: 3.0,
        }

    def analyze(self, user_input: str) -> ComplexityLevel:
        """
        Analyze user input and determine complexity level.

        Args:
            user_input: The natural language input from user

        Returns:
            ComplexityLevel: The recommended complexity level
        """
        if not user_input:
            return ComplexityLevel.MID

        input_lower = user_input.lower()
        word_count = len(user_input.split())

        scores = {
            ComplexityLevel.VERY_SHORT: 0,
            ComplexityLevel.SHORT: 0,
            ComplexityLevel.MID: 0,
            ComplexityLevel.LONG: 0,
        }

        for level, keywords in self.COMPLEXITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in input_lower:
                    scores[level] += self._keyword_weights[level]

        if word_count <= 10:
            scores[ComplexityLevel.VERY_SHORT] += 2
            scores[ComplexityLevel.SHORT] += 1

        if word_count > 50:
            scores[ComplexityLevel.MID] += 1

        if word_count > 100:
            scores[ComplexityLevel.MID] += 2
            scores[ComplexityLevel.LONG] += 1

        if word_count > 200:
            scores[ComplexityLevel.LONG] += 3

        if self._has_multiple_requirements(input_lower):
            scores[ComplexityLevel.MID] += 2
            scores[ComplexityLevel.LONG] += 1

        if self._has_enterprise_indicators(input_lower):
            scores[ComplexityLevel.LONG] += 3

        max_score = max(scores.values())
        if max_score == 0:
            return ComplexityLevel.MID

        for level, score in scores.items():
            if score == max_score:
                return level

        return ComplexityLevel.MID

    def _has_multiple_requirements(self, text: str) -> bool:
        """Check if text contains multiple requirements or steps."""
        patterns = [
            r"\b(and|also|additionally)\b.*\b(need|require|must)\b",
            r"\bstep \d+\b",
            r"\bfirst.*second.*third\b",
            r"\bmultiple\b",
            r"\bseveral\b",
        ]
        return any(re.search(p, text) for p in patterns)

    def _has_enterprise_indicators(self, text: str) -> bool:
        """Check for enterprise-level indicators."""
        enterprise_keywords = [
            "enterprise",
            "production",
            "scalable",
            "robust",
            "security",
            "compliance",
            "audit",
            "monitoring",
            "logging",
            "multi-tenant",
            "api",
            "integration",
            "workflow",
            "automation",
            "system",
        ]
        return sum(1 for kw in enterprise_keywords if kw in text) >= 2

    def get_complexity_description(self, level: ComplexityLevel) -> str:
        """
        Get human-readable description of complexity level.

        Args:
            level: The complexity level

        Returns:
            str: Description of the complexity level
        """
        descriptions = {
            ComplexityLevel.VERY_SHORT: "Minimal, direct, command-style prompt",
            ComplexityLevel.SHORT: "Clear and focused, light structure",
            ComplexityLevel.MID: "Balanced detail with context and constraints",
            ComplexityLevel.LONG: "Fully structured, production-grade prompt",
        }
        return descriptions.get(level, descriptions[ComplexityLevel.MID])

    def analyze_with_details(self, user_input: str) -> dict[str, Any]:
        """
        Analyze input and return detailed results.

        Args:
            user_input: The natural language input

        Returns:
            dict: Contains level, description, word_count, and factors
        """
        level = self.analyze(user_input)
        return {
            "level": level,
            "description": self.get_complexity_description(level),
            "word_count": len(user_input.split()),
            "char_count": len(user_input),
        }


def analyze_complexity(user_input: str) -> ComplexityLevel:
    """
    Convenience function to analyze complexity.

    Args:
        user_input: The user input string

    Returns:
        ComplexityLevel: The recommended complexity level
    """
    analyzer = ComplexityAnalyzer()
    return analyzer.analyze(user_input)
