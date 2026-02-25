# Prompt Generator Agent ChangeLog

---

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-02-25

### Added

- **5 Output Modes**: General LLM, Custom GPT, Agent, JSON, Action Schema (OpenAPI)
- **Prompt Hardening Layer**: Anti-hallucination safeguards, clarification rules, edge case handling
- **Risk Detection**: Analyze prompts for failure points, ambiguity, and hallucination risks
- **Metadata Generation**: Version tracking, complexity analysis, model targeting
- **Memory Integration**: Prompt engineering notes for better outputs
- **CLI Mode Selection**: Interactive mode selection (1-5)
- **UI Mode Selector**: Sidebar dropdown for mode selection
- **JSON Output Support**: Toggle between Markdown and JSON output
- **Dynamic Pipeline**: Skips risk/hardening for general_llm mode for faster execution

### Changed

- **Project Renamed**: Prompt Generator Agent → Prompt Optimization Agent
- **Package Structure**: Renamed to `prompt-optimization-agent`
- **CLI Entry Points**: `prompt-optimization-cli`, `prompt-optimization-ui`
- **Improved Exporter**: Now includes metadata, hardened prompt, and risk analysis in output files

### Fixed

- **Timeout Configuration**: Increased default timeout to 180 seconds
- **Import Paths**: Fixed module imports for CLI and UI

### Documentation

- **MkDocs Setup**: Material theme with organized navigation
- **Updated Docs**: Setup, usage, API reference, testing guides
- **New Structure**: Guides, Reference, Product, Planning sections

---

## [2.0.2] - 2026-01-20

### Version 2.0.2 Added, Updated

- Added building custom gpt notes in memory dir.
- Added building custom gpt notes in memory memory_manager
- Added test_memory_loading_verification to test loaded memory
- Updated formatting issues in markdown files.

## [2.0.1] - 2026-01-16

### Version 2.0.1 Updated

- Updated UI to show full logs in detail for each step update (Running generator, Running reviewer, Running test  case generator).
- Finalized output format in ui only generate in UI so that user can easily copy paste instead of saving file.

## [2.0.0] - 2026-01-16

### Version 2.0.0 Added

- Added OpenAI SDK provider integration
- Added comprehensive unit tests for new provider and exporter modules
- Updated documentation to reflect new features and usage instructions
- Improved logging for better debugging and monitoring
- Fixed minor bugs in memory management and prompt generation
- Enhanced .gitignore to exclude additional temporary files
- Updated dependencies in requirements.txt and pyproject.toml
- Refined README and docs for clarity and completeness
- Prepared for next release with version bump

## [1.0.0] - 2026-01-15

### Version 1.0.0 Added

- Added initial version of prompt generator agent.
