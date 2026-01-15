# Setup Guide

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) (for local LLM support)

## Installation Steps
1. **Clone and Enter**:
   ```bash
   git clone <repo_url>
   cd prompt-generator-agent
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
Edit `src/config/settings.py` to change the active provider:

### LiteLLM (Cloud)
```python
PROVIDER = "litellm"
MODEL_NAME = "gemini/gemini-2.0-flash"
```

### Ollama (Local)
```python
PROVIDER = "ollama"
MODEL_NAME = "llama3.1:8b"
```
Ensure the Ollama server is running locally before execution.

## Running the Application

### CLI
```bash
python src/cli.py
```

### UI
```bash
streamlit run src/ui.py
```

## Adding Custom Prompts

Replace the content in the `.md` files in `src/agent/` with your instructions.