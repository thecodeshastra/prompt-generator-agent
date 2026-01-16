"""Result exporter utility module."""

import os
from datetime import datetime
from typing import Any, Dict, Optional

from core.utils.logger import logger

# Define the output directory as a constant
# Get the root directory (assuming this file is in src/core/utils)
_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUTPUT_DIR = os.path.join(_ROOT_DIR, "output")

def save_result_to_markdown(result: Dict[str, Any], user_input: str) -> Optional[str]:
    """
    Export the pipeline result to a formatted markdown file.

    Args:
        result (Dict[str, Any]): The complete result dictionary from the orchestrator.
        user_input (str): The original user request string.

    Returns:
        Optional[str]: The absolute path to the saved file, or None if saving failed.
    """
    try:
        if not os.path.exists(OUTPUT_DIR):
            try:
                os.makedirs(OUTPUT_DIR)
            except OSError as e:
                logger.error(f"Failed to create output directory {OUTPUT_DIR}: {e}")
                return None

        # Generate filename: title + datetime
        # Extract a short title from user input (first 3 words)
        clean_input = "".join(c for c in user_input if c.isalnum() or c.isspace()).strip()
        title = "_".join(clean_input.split()[:3]).lower() or "prompt"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Build markdown content
        md_content = f"# Prompt Generation Result: {clean_input[:50]}\n\n"
        md_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md_content += f"**Original Request:** {user_input}\n\n"
        
        md_content += "---\n\n"
        md_content += "## 1. Final Generated Prompt\n\n"
        md_content += f"```markdown\n{result.get('generated_prompt', 'N/A')}\n```\n\n"
        
        md_content += "## 2. Review Verdict\n\n"
        review = result.get("review", {})
        md_content += f"- **Approved:** {'✅ Yes' if review.get('approved') else '❌ No'}\n"
        md_content += f"- **Rating:** {review.get('rating', 'N/A')}/5\n"
        md_content += f"- **Feedback:** {review.get('feedback', 'N/A')}\n\n"
        
        if result.get("test_cases"):
            md_content += "## 3. Test Cases\n\n"
            for i, tc in enumerate(result["test_cases"], 1):
                md_content += f"### Test Case {i}\n"
                md_content += f"- **Input:** {tc.get('input', 'N/A')}\n"
                md_content += f"- **Expected Output:** {tc.get('expected_output', 'N/A')}\n"
                if tc.get("rubric"):
                    md_content += f"- **Rubric:** {tc.get('rubric')}\n"
                md_content += "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        logger.info(f"Result saved to {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Failed to save result to markdown: {e}")
        return None
