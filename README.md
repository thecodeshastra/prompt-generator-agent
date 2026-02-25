# Prompt Optimization Agent

A production-grade prompt optimization and reliability engine that transforms raw ideas into structured, validated, and enterprise-ready AI instructions.

## Key Features

- **6-Stage Pipeline**: Optimize → Review → Risk Detection → Hardening → Test Cases → Metadata
- **5 Output Modes**:
  - `general_llm` - Standard prompts for ChatGPT, Claude, etc.
  - `custom_gpt` - GPT Builder configuration format
  - `agent` - AI agent system prompts
  - `json` - Structured JSON for APIs/automation
  - `action_schema` - OpenAPI 3.1.0 schemas for tool-calling
- **Prompt Hardening**: Anti-hallucination safeguards, clarification rules, edge case handling
- **Risk Detection**: Identify failure points, ambiguity, and hallucination risks
- **Multi-Provider Support**: OpenAI, Gemini, Anthropic (via LiteLLM), local models (via Ollama)
- **Memory Integration**: Prompt engineering notes for better outputs

## Quick Start

```bash
# Clone and install
git clone <repo-url>
cd prompt-optimization-agent
pip install -e .

# Run CLI
prompt-optimization-cli

# Or run UI
streamlit run src/prompt_optimization_agent/ui.py
```

## Documentation

For detailed guides and reference:

| Guide | Description |
|-------|-------------|
| [Setup Guide](docs/guides/setup.md) | Installation and configuration |
| [Usage Guide](docs/guides/usage.md) | CLI and UI usage |
| [API Reference](docs/reference/api.md) | Core classes and functions |
| [Testing](docs/guides/testing.md) | Testing procedures |
| [Output Format](docs/reference/outputs.md) | Result file structure |

## Architecture

```
User Input → Optimize → Review → Risk Detection → Hardening → Test Cases → Metadata → Output
```

## Project Structure

```
src/prompt_optimization_agent/
├── agent/
│   ├── orchestrator.py       # Pipeline orchestration
│   ├── prompt_generator.py   # Prompt optimizer
│   ├── prompt_hardener.py    # Hardening agent
│   ├── prompt_reviewer.py    # Review agent
│   ├── risk_detector.py     # Risk analysis
│   ├── test_case_generator.py
│   ├── prompts/              # Agent prompts
│   └── memory/               # Memory system
├── core/
│   ├── config/               # Configuration
│   ├── providers/            # LLM providers
│   └── utils/                # Utilities
└── ui.py                    # Streamlit UI
```

## License

MIT
