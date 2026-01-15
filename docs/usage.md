# Usage Guide

The Prompt Generator Agent can be used through two interfaces:

## 1. CLI Usage
Run the interactive command-line interface:
```bash
python src/cli.py
```
- **Interact**: Enter your prompt description when prompted.
- **Workflow**: The CLI will show generation progress, print the review results, and list test cases if approved.
- **Export**: Results are automatically saved to the `output/` directory.

## 2. Web UI (Streamlit)
Launch the graphical interface for a more visual experience:
```bash
streamlit run src/ui.py
```
- **Live Status**: Uses the `st.status` component to show real-time progress of the 3-stage pipeline.
- **Visual Review**: See ratings and approvals with clear color-coded indicators.
- **Test Case Expanders**: Browse generated test cases in an organized, collapsible view.

## 3. Review Process
- If an agent rates the prompt **below 4/5**, the system will attempt an iterative improvement automatically (up to 3 times).
- Feedback from the review agent is used to refine the next generation.

## 4. Output Management
- All final results are stored in `output/` as Markdown files.
- Each file includes the final prompt, the reviewer's audit, and the generated test cases.
g memory
3. **Review**: AI evaluates the prompt (rating 1-5, approval)
4. **Test Cases**: If approved, AI generates validation examples

## Memory Integration