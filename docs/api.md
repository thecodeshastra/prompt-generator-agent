# API Reference

## Core Classes

### BaseProvider

Abstract base class for AI providers.

**Methods:**
- `generate(prompt: str, system_prompt: Optional[str] = None) -> str`: Generate a response from the AI provider.

**Example:**
```python
from interfaces.base_provider import BaseProvider

class MyProvider(BaseProvider):
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # Implementation
        return "response"
```

### BaseAgent

Abstract base class for agents.

**Methods:**
- `run(input_data: str) -> Dict[str, Any]`: Run the agent with input data.

**Example:**
```python
from interfaces.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def run(self, input_data: str) -> Dict[str, Any]:
        # Implementation
        return {"result": "data"}
```

Main entry point for the pipeline.

**Methods:**
- `__init__(provider: Optional[BaseProvider] = None)`: Initialize with optional custom provider.
- `run_pipeline(user_input: str) -> Dict[str, Any]`: Run full 3-stage pipeline.

**Returns:** Complete result dict with generated_prompt, review, test_cases (if approved).

**Example:**
```python
from agent.orchestrator import PromptGeneratorOrchestrator

orchestrator = PromptGeneratorOrchestrator()
result = orchestrator.run_pipeline("Generate a prompt for summarization")
```

## Configuration

Settings are loaded from `src/config/settings.py`. Key variables:

- `PROVIDER`: AI provider to use ("litellm" only)
- `MODEL_NAME`: Model identifier (e.g., "gpt-4", "gemini/gemini-1.5-pro", "claude-3")
- `TEMPERATURE`: Generation temperature (0.0-1.0)
- `MAX_TOKENS`: Maximum tokens per response
- `USE_MEMORY`: Enable/disable memory for generation (bool)

## Provider

### LiteLLMProvider

Unified access to 100+ LLMs via LiteLLM.

**Init:** `__init__(model_name, temperature, max_tokens, timeout, max_retries, retry_backoff)`

**Supported Models:** Any model supported by LiteLLM (OpenAI, Google, Anthropic, etc.)
- OpenAI: "gpt-4", "gpt-3.5-turbo"
- Google: "gemini/gemini-1.5-pro"
- Anthropic: "claude-3-opus"
- And 100+ more!

## Memory System

### MemoryManager

Manages prompt engineering notes from Markdown.

**Methods:**
- `__init__(memory_file: str = "prompt_engineering_notes.md")`: Load notes file.
- `get_relevant_notes(query: str, max_chars: int = 1000) -> str`: Get relevant notes excerpt.
- `get_all_notes() -> str`: Get full notes content.

**Notes Format:** Markdown with headers for sections.

**Example:**
```markdown
# Prompt Optimization
Use specific examples and clear instructions.

# Custom GPT Building
Follow these guidelines for creating custom models...
```

## Utilities

### Logger

Structured logging utility.

**Usage:** `from core.utils.logger import logger; logger.info("message")`

## Benchmark PDF Integration

Test case generation automatically reads `src/agent/benchmark.pdf` using PyPDF for quality guidelines.

**Requirements:** Install `pypdf>=4.0.0`

## Error Handling

All methods include try/except blocks with logging. Failures return appropriate error dicts.

## Type Hints

All functions use full type hints for better IDE support and documentation.