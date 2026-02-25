# Usage Guide

The Prompt Optimization Agent can be used through two interfaces:

## 1. CLI Usage

Run the interactive command-line interface:

```bash
python -m prompt_optimization_agent.cli
```

- **Mode Selection**: Choose from 5 output modes (General LLM, Custom GPT, Agent, JSON, Action Schema)
- **Output Format**: Choose between Markdown or JSON output
- **Workflow**: The CLI shows optimization progress, review results, risk analysis, and test cases
- **Export**: Results are automatically saved to the `output/` directory

## 2. Web UI (Streamlit)

Launch the graphical interface:

```bash
streamlit run src/prompt_optimization_agent/ui.py
```

- **Mode Selector**: Choose output mode from sidebar dropdown
- **Output Format**: Toggle between Markdown and JSON
- **Live Status**: Uses the `st.status` component to show real-time pipeline progress
- **Visual Review**: See ratings and approvals with clear color-coded indicators
- **Risk Analysis**: View detected risks and severity levels
- **Metadata**: See version, mode, and complexity information

## 3. Pipeline Stages

The optimization pipeline runs through these stages:

1. **Optimize**: Generate prompt based on user input and selected mode
2. **Review**: Evaluate prompt quality and provide feedback
3. **Risk Detection**: Analyze for potential failure points and risks
4. **Hardening**: Add safety rules and edge case handling
5. **Test Cases**: Generate validation test cases
6. **Metadata**: Attach version and complexity information

## 4. Review Process

- If an agent rates the prompt **below 4/5**, the system will attempt iterative improvement automatically (up to 3 times)
- Feedback from the review agent is used to refine the next generation

## 5. Output Management

- All final results are stored in `output/` as Markdown files
- Each file includes: final prompt, review audit, risk analysis, test cases, and metadata
- JSON output is also available via CLI or UI

## 6. Mode Selection

| Mode | Use Case |
|------|----------|
| `general_llm` | Standard prompts for ChatGPT, Claude, Gemini |
| `custom_gpt` | GPT Builder configuration with instructions |
| `agent` | AI agent system prompts with tool definitions |
| `json` | Structured JSON for API/automation workflows |
| `action_schema` | OpenAPI 3.1.0 schemas for Custom GPT Actions |

## 7. Memory Integration

- The system uses memory for prompt engineering notes
- Notes are stored in `src/prompt_optimization_agent/agent/memory` directory
- Prompt templates are in `src/prompt_optimization_agent/agent/prompts` directory
