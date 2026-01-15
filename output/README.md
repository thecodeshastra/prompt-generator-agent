# Prompt Generator Outputs

This directory contains the automatically generated results from the Prompt Generator Agent.

## Automatic Generation
Every time a prompt is generated and reviewed (using `cli.py` or `ui.py`), a new markdown file is created here.

### Filename Format
- Pattern: `{short_title}_{timestamp}.md`
- Example: `joke_writer_20260115_224002.md`

## File Structure
Each generated file contains:
- **Final Generated Prompt**: The copy-paste ready prompt optimized using a specific framework.
- **Review Verdict**: The approval status, rating (1-5), and qualitative feedback from the review agent.
- **Test Cases**: 5 specific scenarios to test the generated prompt, including inputs, expected results, and scoring rubrics.