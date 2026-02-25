# Prompt Optimization Outputs

This directory contains automatically generated results from the Prompt Optimization Agent.

## Automatic Generation

Every time a prompt is optimized, a new markdown file is created.

### Filename Format

- Pattern: `{short_title}_{timestamp}.md`
- Example: `joke_writer_20260115_224002.md`

## File Structure

Each generated file contains:

1. **Final Optimized Prompt**: The copy-paste ready prompt
2. **Review Verdict**: Approval status, rating (1-5), feedback
3. **Risk Analysis**: Risk score, level, identified risks
4. **Test Cases**: 5 scenarios to validate the prompt
5. **Metadata**: Version, mode, complexity level, target model

## JSON Output

When JSON output is selected, the result contains:

```json
{
  "prompt": "optimized prompt text",
  "metadata": {
    "version": "1.0.0",
    "mode": "agent",
    "complexity_level": "mid",
    "target_model": "auto-detect"
  },
  "risk_analysis": {
    "overall_risk_score": 3,
    "risk_level": "low",
    "risks": []
  }
}
```
