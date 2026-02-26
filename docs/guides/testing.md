# Testing Guide

This document outlines procedures for testing the Prompt Optimization Agent.

## 1. Automated Unit Tests

The project includes comprehensive unit tests in `tests/` directory. Tests use mocks for LLM providers.

### Using Pytest (Recommended)

```bash
# Install test dependencies
uv pip install pytest pytest-mock pytest-cov

# Run the full suite
uv run pytest tests/
```

### Using Unittest (Built-in)

```bash
python3 -m unittest discover tests

# Run with verbose output
python3 -m unittest -v discover tests
```

---

## 2. Manual Verification

### CLI Testing

```bash
python -m prompt_optimization_agent.cli
```

**Verification Points:**

- [ ] Mode selection works (1-5 options)
- [ ] Pipeline initializes without errors
- [ ] Iteration status is displayed
- [ ] Risk analysis is shown
- [ ] Hardened prompt is displayed
- [ ] Output format toggle works (m/j)

### Web UI Testing

```bash
streamlit run src/prompt_optimization_agent/ui.py
```

**Verification Points:**

- [ ] Mode selector in sidebar works
- [ ] Output format toggle works
- [ ] Progress bars/status update correctly
- [ ] Risk analysis section displays
- [ ] Metadata section displays

---

## 3. Code Style & Linting

```bash
# Check for style issues
uv run ruff check .

# Automatically fix minor issues
uv run ruff check . --fix
```

## 4. Test Structure

- `tests/test_agents.py`: Tests for PromptOptimizer, PromptHardener, RiskDetector, PromptReviewer, TestCaseGenerator, and Orchestrator
- `tests/test_providers.py`: Tests for OpenAI and Ollama providers
- `tests/test_exporter.py`: Tests for markdown generation
- `tests/test_core_utils.py`: Tests for InputConfig, ComplexityAnalyzer, MetadataGenerator
- `tests/test_memory_loading_verification.py`: Tests for MemoryManager

## 5. New Features Testing

### Mode Selection

Test all 5 output modes:

- `general_llm` - Standard prompts
- `custom_gpt` - GPT Builder config
- `agent` - AI agent prompts
- `json` - JSON output
- `action_schema` - OpenAPI schemas

### Risk Detection

Verify risk analysis returns:

- `overall_risk_score` (0-10)
- `risk_level` (low/medium/high)
- `risks` list with categories
- `recommendations` list

### Prompt Hardening

Verify hardening adds:

- Anti-hallucination safeguards
- Clarification rules
- Edge case handlers
