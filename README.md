# Prompt Generator Agent

A modular, production-grade AI agent designed to **generate, review, and test prompts** using an iterative 3-stage pipeline. Optimized for professional prompt engineering, it supports 100+ LLMs via LiteLLM and provides dedicated support for local execution via Ollama.

## 🚀 Key Features

- **3-Stage Pipeline**: 
    1. **Generate**: Creates a structured prompt using frameworks like CLEAR, RCT, or CRISP.
    2. **Review**: Evaluates the prompt against professional standards (JSON-based audit).
    3. **Test Cases**: Generates high-quality test scenarios for the approved results.
- **Multi-Provider Support**: Seamlessly switch between OpenAI, Gemini, Anthropic (via LiteLLM), or local models (via Ollama).
- **System Prompt Architecture**: Every agent uses a dedicated system prompt for superior instruction adherence.
- **Robust Parsing**: Advanced JSON extraction with regex fallbacks and code-block sensing.
- **Result Export**: Automatically saves every run into timestamped markdown files in the `output/` directory.

## 🛠️ Setup & Configuration

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com/) (if running locally)

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd prompt-generator-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Create your environment file
cp .env.example .env
```
> [!IMPORTANT]
> A `.env` file must be present in the root directory for the application to load configurations and API keys correctly.

### LLM Configuration
Edit the `.env` file you just created:

#### Using Local Ollama (Default)
1. Ensure Ollama is running: `ollama run llama3.1:8b`
2. Configure settings:
   ```python
   PROVIDER = "ollama"
   MODEL_NAME = "llama3.1:8b"
   ```

#### Using LiteLLM (Cloud Providers)
1. Configure settings:
   ```python
   PROVIDER = "litellm"
   MODEL_NAME = "gemini/gemini-pro" # or "openai/gpt-4"
   ```
2. Add your API keys to the `.env` file.

## 🖥️ Usage

### Command Line Interface
Run the interactive CLI to generate prompts:
```bash
python src/cli.py
```

### Streamlit Web UI
Launch the graphical interface:
```bash
streamlit run src/ui.py
```

## 📁 Project Structure
- `src/agent/`: Core agent logic (Generators, Reviewers, Test Architects).
- `src/core/providers/`: LLM interface implementations.
- `src/core/utils/`: Exporters, loggers, and parsing utilities.
- `output/`: Automatically saved results in Markdown format.
