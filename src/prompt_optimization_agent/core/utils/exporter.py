"""Result exporter utility module."""

from datetime import datetime
from pathlib import Path
from typing import Any

from .logger import logger

_ROOT_DIR = Path(__file__).resolve().parents[3]
OUTPUT_DIR = _ROOT_DIR / "output"


def save_result_to_markdown(result: dict[str, Any], user_input: str) -> str | None:
    """
    Export the pipeline result to a formatted markdown file.

    Args:
        result (Dict[str, Any]): The complete result dictionary from the orchestrator.
        user_input (str): The original user request string.

    Returns:
        Optional[str]: The absolute path to the saved file, or None if saving failed.
    """
    try:
        if not OUTPUT_DIR.exists():
            try:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.error(f"Failed to create output directory {OUTPUT_DIR}: {e}")
                return None

        clean_input = "".join(c for c in user_input if c.isalnum() or c.isspace()).strip()
        title = "_".join(clean_input.split()[:3]).lower() or "prompt"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}.md"
        filepath = OUTPUT_DIR / filename

        md_content = f"# Prompt Optimization Result: {clean_input[:50]}\n\n"
        md_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md_content += f"**Original Request:** {user_input}\n\n"

        # Metadata
        md_content += "---\n\n## Metadata\n\n"
        metadata = result.get("metadata", {})
        md_content += f"- **Version:** {metadata.get('version', 'N/A')}\n"
        md_content += f"- **Mode:** {metadata.get('mode', 'N/A')}\n"
        md_content += f"- **Complexity:** {metadata.get('complexity_level', 'N/A')}\n"
        md_content += f"- **Risk Score:** {metadata.get('risk_score', 'N/A')}\n"
        md_content += f"- **Risk Level:** {metadata.get('risk_level', 'N/A')}\n\n"

        md_content += "---\n\n## 1. Final Generated Prompt\n\n"
        md_content += f"```markdown\n{result.get('generated_prompt', 'N/A')}\n```\n\n"

        # Hardened prompt (if available)
        if result.get("hardened_prompt") and result.get("hardened_prompt") != result.get("generated_prompt"):
            md_content += "---\n\n## 2. Hardened Prompt\n\n"
            md_content += f"```markdown\n{result.get('hardened_prompt', 'N/A')}\n```\n\n"
            section_num = 3
        else:
            section_num = 2

        md_content += f"---\n\n## {section_num}. Review Verdict\n\n"
        review = result.get("review", {})
        md_content += f"- **Approved:** {'✅ Yes' if review.get('approved') else '❌ No'}\n"
        md_content += f"- **Rating:** {review.get('rating', 'N/A')}/5\n"
        md_content += f"- **Feedback:** {review.get('feedback', 'N/A')}\n\n"

        # Risk Analysis
        risk = result.get("risk_analysis", {})
        if risk and not risk.get("skipped"):
            md_content += f"---\n\n## {section_num + 1}. Risk Analysis\n\n"
            md_content += f"- **Risk Score:** {risk.get('overall_risk_score', 'N/A')}/10\n"
            md_content += f"- **Risk Level:** {risk.get('risk_level', 'N/A')}\n"
            md_content += f"- **Summary:** {risk.get('summary', 'N/A')}\n\n"
            if risk.get("risks"):
                md_content += "**Identified Risks:**\n"
                for r in risk.get("risks", [])[:5]:
                    md_content += f"- **{r.get('category')}** ({r.get('severity')}): {r.get('description')}\n"
                md_content += "\n"

        # Test Cases
        if result.get("test_cases"):
            test_case_start = section_num + 2 if risk and not risk.get("skipped") else section_num + 1
            md_content += f"---\n\n## {test_case_start}. Test Cases\n\n"
            for i, tc in enumerate(result["test_cases"], 1):
                md_content += f"### Test Case {i}\n"
                md_content += f"- **Input:** {tc.get('input', 'N/A')}\n"
                md_content += f"- **Expected Output:** {tc.get('expected_output', 'N/A')}\n"
                if tc.get("rubric"):
                    md_content += f"- **Rubric:** {tc.get('rubric')}\n"
                md_content += "\n"

        with filepath.open("w", encoding="utf-8") as f:
            f.write(md_content)

        logger.info(f"Result saved to {filepath}")
        return str(filepath)

    except Exception as e:
        logger.error(f"Failed to save result to markdown: {e}")
        return None
