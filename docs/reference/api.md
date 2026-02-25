# API Reference

## Core Classes

### BaseProvider

Abstract base class for AI providers.

**Methods:**

- `generate(prompt: str, system_prompt: Optional[str] = None) -> str`: Generate a response from the AI provider.

**Example:**

```python
from prompt_optimization_agent.interfaces.base_provider import BaseProvider

class MyProvider(BaseProvider):
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # Implementation
        return "response"
```

### BaseAgent

Abstract base class for agents.

**Methods:**

- `run(input_data: str) -> Dict[str, Any]`: Run the agent with input data.

### PromptOptimizationOrchestrator

Main entry point for the pipeline.

**Methods:**

- `__init__(provider: Optional[BaseProvider] = None, mode: PromptMode = PromptMode.GENERAL_LLM)`: Initialize with optional custom provider and output mode.
- `run_pipeline(user_input: str, max_iterations: int = 3, mode: Optional[PromptMode] = None, output_format: str = "markdown") -> Dict[str, Any]`: Run full pipeline.

**Returns:** Complete result dict with generated_prompt, hardened_prompt, review, risk_analysis, test_cases, metadata.

**Example:**

```python
from prompt_optimization_agent.agent.orchestrator import PromptOptimizationOrchestrator
from prompt_optimization_agent.core.config.input_config import PromptMode

orchestrator = PromptOptimizationOrchestrator(mode=PromptMode.AGENT)
result = orchestrator.run_pipeline("Generate a system prompt for an AI agent")
```

### PromptOptimizer

Agent for generating optimized prompts with mode support.

**Methods:**

- `__init__(provider: BaseProvider, use_memory: bool = True, mode: PromptMode = PromptMode.GENERAL_LLM)`
- `set_mode(mode: PromptMode)`: Change output mode
- `run(user_input: str, previous_prompt: Optional[str] = None, feedback: Optional[str] = None) -> Dict[str, Any]`

### PromptHardener

Agent for hardening prompts with safety rules and edge case handling.

**Methods:**

- `run(prompt: str) -> Dict[str, Any]`: Returns hardened_prompt

### RiskDetector

Agent for detecting risks in prompts.

**Methods:**

- `run(prompt: str) -> Dict[str, Any]`: Returns risk analysis with overall_risk_score, risk_level, risks, summary

### PromptReviewer

Agent for reviewing prompt quality.

**Methods:**

- `run(prompt: str) -> Dict[str, Any]`: Returns approved, rating, feedback

### TestCaseGenerator

Agent for generating validation test cases.

**Methods:**

- `run(prompt: str) -> Dict[str, Any]`: Returns test_cases list

## Configuration

### InputConfig

Configuration class for prompt optimization input.

```python
from prompt_optimization_agent.core.config.input_config import InputConfig, PromptMode, ComplexityLevel

config = InputConfig(
    user_input="my prompt idea",
    mode=PromptMode.AGENT,
    complexity=ComplexityLevel.LONG,
    target_model="gpt-4"
)
```

### PromptMode Enum

Output modes for prompt optimization:

- `GENERAL_LLM` - Standard prompts
- `CUSTOM_GPT` - GPT Builder config
- `AGENT` - AI agent prompts
- `JSON` - JSON output
- `ACTION_SCHEMA` - OpenAPI schemas

### ComplexityLevel Enum

Auto-detected complexity levels:

- `VERY_SHORT` - Minimal command
- `SHORT` - Light structure
- `MID` - Balanced detail
- `LONG` - Production-grade

Settings are loaded from `src/prompt_optimization_agent/config/settings.py`. Key variables:

- `PROVIDER`: AI provider ("litellm", "ollama", "openai")
- `MODEL_NAME`: Model identifier
- `TEMPERATURE`: Generation temperature
- `MAX_TOKENS`: Maximum tokens
- `USE_MEMORY`: Enable/disable memory

## Providers

### LiteLLMProvider

Unified access to 100+ LLMs via LiteLLM.

### OpenAIProvider

Native implementation using official OpenAI SDK.

### OllamaProvider

Native implementation for local LLMs.

## Memory System

### MemoryManager

Manages prompt engineering notes from Markdown files.

**Methods:**

- `get_relevant_notes(query: str, max_chars: int = 1000) -> str`: Get relevant notes
- `get_all_notes() -> str`: Get all notes

## Utilities

### ComplexityAnalyzer

Auto-detects prompt complexity.

```python
from prompt_optimization_agent.core.utils.complexity_analyzer import analyze_complexity

level = analyze_complexity("create an enterprise production system")
```

### MetadataGenerator

Generates metadata for optimized prompts.

```python
from prompt_optimization_agent.core.utils.metadata_generator import generate_metadata

metadata = generate_metadata(mode="agent", target_model="gpt-4")
```

### Logger

```python
from prompt_optimization_agent.core.utils.logger import logger
logger.info("message")
```

## Error Handling

All methods include try/except blocks with logging. Failures return appropriate error dicts.
