"""Result exporter utility module."""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from core.utils.logger import logger

def save_result_to_markdown(result: Dict[str, Any], user_input: str, output_dir: str = "output"):
    """
    Save the pipeline result to a markdown file.

    Args:
        result (Dict[str, Any]): The pipeline result dictionary.
        user_input (str): The original user input description.
        output_dir (str): The directory to save the file in.
    """
    try:
        # Ensure output directory exists
        # Get the root directory (assuming this file is in src/core/utils)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        abs_output_dir = os.path.join(root_dir, output_dir)
        
        if not os.path.exists(abs_output_dir):
            os.makedirs(abs_output_dir)

        # Generate filename: title + datetime
        # Extract a short title from user input (first 3 words)
        clean_input = "".join(c for c in user_input if c.isalnum() or c.isspace()).strip()
        title = "_".join(clean_input.split()[:3]).lower() or "prompt"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{title}_{timestamp}.md"
        filepath = os.path.join(abs_output_dir, filename)

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
