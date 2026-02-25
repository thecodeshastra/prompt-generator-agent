# Setup Guide

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com/) (for local LLM support)

## Installation Steps

1. **Clone and Enter**:

   ```bash
   git clone <repo_url>
   cd prompt-optimization-agent
   ```

2. **Environment Setup**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate  # Windows
   pip install -e .
   ```

3. **Configure Environment**:
   Copy the example environment file and add your credentials:

   ```bash
   cp .env.example .env
   ```

   > [!WARNING]
   > The `.env` file is mandatory. If you are using `litellm` (Cloud providers), you **must** provide the corresponding API keys in this file.

   *Note: For local Ollama usage, no API keys are required, but the `.env` file should still exist to load default settings.*

## LLM Configuration

Edit `src/prompt_optimization_agent/config/settings.py` to change the active provider:

### LiteLLM (Cloud)

```python
PROVIDER = "litellm"
MODEL_NAME = "gemini/gemini-2.0-flash" 
```

### OpenAI SDK (Official or Compatible)

```python
PROVIDER = "openai"
MODEL_NAME = "gpt-4o" # or any compatible model
OPENAI_BASE_URL="https://openrouter.ai/api/v1" # you can change this to any other provider with updating their api key
```

You can also set `OPENAI_BASE_URL` in your `.env` file to use OpenAI-compatible services like OpenRouter, DeepSeek, or LiteLLM Proxy.

### Ollama (Local)

```python
PROVIDER = "ollama"
MODEL_NAME = "llama3.1:8b"
```

Ensure the Ollama server is running locally before execution.

> [!NOTE]
> You can also confirm all other env variables in `.env` file. Like MAX_TOKENS, TEMPERATURE, TIMEOUT_SECONDS, etc. Just in case you want to change them.

## Running the Application

### CLI

```bash
python -m prompt_optimization_agent.cli
# or
prompt-optimization-cli
```

### UI

```bash
streamlit run src/prompt_optimization_agent/ui.py
```

## Output Modes

The Prompt Optimization Agent supports 5 output modes:

| Mode | Description |
|------|-------------|
| `general_llm` | Standard prompts for ChatGPT, Claude, etc. |
| `custom_gpt` | GPT Builder configuration format |
| `agent` | AI agent system prompts |
| `json` | Structured JSON for APIs/automation |
| `action_schema` | OpenAPI 3.1.0 schemas for tool-calling |

## Adding Custom Prompts

Replace the content in the `.md` files in `src/prompt_optimization_agent/agent/prompts` with your instructions.
Default templates are already optimized but can be customized as needed.
