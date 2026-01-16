# Testing Guide

This document outlines the procedures for testing the Prompt Generator Agent to ensure reliability, performance, and production-grade standards.

## 1. Automated Unit Tests
The project includes a comprehensive suite of unit tests in the `tests/` directory. These tests use mocks for all LLM providers, so they do **not** require API keys or an internet connection.

### Using Pytest (Recommended)
Pytest provides a cleaner output and more powerful debugging tools.
```bash
# Install test dependencies
pip install pytest pytest-mock

# Run the full suite
python3 -m pytest tests/
```

### Using Unittest (Built-in)
If you prefer not to install external dependencies, use the built-in `unittest` framework.
```bash
# Run all tests using discovery
python3 -m unittest discover tests

# Run with verbose output
python3 -m unittest -v discover tests
```

---

## 2. Manual Verification
Manual testing is essential for verifying CLI output formatting and UI responsiveness.

### CLI Testing
```bash
python3 src/cli.py
```
**Verification Points:**
- [ ] Pipeline initializes without errors.
- [ ] Iteration status is displayed clearly.
- [ ] On success, only the save path is printed (no full prompt dump).
- [ ] On failure, a clean `❌ ERROR` message is shown.

### Web UI Testing
```bash
streamlit run src/ui.py
```
**Verification Points:**
- [ ] Progress bars/status indicators update correctly.
- [ ] Results are displayed in expandable sections.
- [ ] The "Automatically saved" notification appears on success.

---

## 3. Code Style & Linting
We use `ruff` to maintain production-grade code quality and PEP 8 compliance.

```bash
# Install ruff
pip install ruff

# Check for style issues
ruff check .

# Automatically fix minor issues
ruff check . --fix
```

## 4. Test Structure
- `tests/test_agents.py`: Verifies logic for Generator, Reviewer, and Orchestrator.
- `tests/test_providers.py`: Verifies API integration logic for OpenAI and Ollama.
- `tests/test_exporter.py`: Verifies markdown generation and file saving logic.
