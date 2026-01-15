"""Streamlit UI for the prompt generator agent."""

import sys
import os
import streamlit as st

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from agent.orchestrator import PromptGeneratorOrchestrator
from core.utils.logger import logger
from core.utils.exporter import save_result_to_markdown


def main():
    """
    Main Streamlit app function.
    """
    st.title("Prompt Generator Agent")
    st.markdown("Generate, review, and test prompts with AI assistance.")

    # Initialize orchestrator
    if "orchestrator" not in st.session_state:
        try:
            st.session_state.orchestrator = PromptGeneratorOrchestrator()
        except Exception as e:
            st.error(f"Failed to initialize: {e}")
            return

    # Input section
    st.header("Step 1: Describe Your Prompt")
    user_input = st.text_area(
        "Enter a description of the prompt you want to generate:",
        height=100,
        placeholder="e.g., A prompt for summarizing meeting notes with action items",
    )

    if st.button("Generate Prompt", type="primary"):
        if not user_input.strip():
            st.error("Please enter a description.")
            return

        with st.status("Processing Pipeline...", expanded=True) as status:
            try:
                st.write("Initializing orchestrator...")
                orchestrator = st.session_state.orchestrator
                
                st.write("Running iteration analysis...")
                result = orchestrator.run_pipeline(user_input)

                st.write("Finalizing results...")
                status.update(label="Pipeline Completed!", state="complete", expanded=False)

                # Store result in session
                st.session_state.result = result

                # Display generated prompt
                st.header("Step 2: Generated Prompt")
                generated_prompt = result.get("generated_prompt", "Failed to generate")
                st.text_area(
                    "Generated Prompt:",
                    value=generated_prompt,
                    height=200,
                    disabled=True,
                )

                # Display review
                st.header("Step 3: Review Results")
                review = result.get("review", {})
                approved = review.get("approved", False)
                
                col1, col2 = st.columns(2)
                with col1:
                    if approved:
                        st.success("✅ Approved")
                    else:
                        st.error("❌ Not Approved")
                with col2:
                    st.metric("Rating", f"{review.get('rating', 'N/A')}/5")

                st.text_area(
                    "Reviewer Feedback:",
                    value=review.get("feedback", "No feedback provided."),
                    height=100,
                    disabled=True,
                )

                # Test cases
                st.header("Step 4: Test Cases")
                test_cases = result.get("test_cases")
                
                if approved:
                    if test_cases:
                        st.success(f"Generated {len(test_cases)} test cases")
                        for i, tc in enumerate(test_cases, 1):
                            with st.expander(f"Test Case {i}"):
                                st.markdown(f"**Input:** {tc.get('input', 'N/A')}")
                                st.markdown(f"**Expected Output:** {tc.get('expected_output', 'N/A')}")
                                if tc.get('rubric'):
                                    st.markdown(f"**Rubric:** {tc.get('rubric')}")
                    elif test_cases == []:
                        error_msg = result.get("test_error", "Unknown error in test generation.")
                        st.error(f"Failed to generate test cases: {error_msg}")
                    else:
                        st.info("Test cases were skipped or not yet generated.")
                else:
                    st.warning("No test cases generated because the prompt was not approved.")

                if "error" in result:
                    st.error(f"Pipeline Error: {result['error']}")

                # Save to file
                saved_path = save_result_to_markdown(result, user_input)
                if saved_path:
                    st.info(f"📁 Result automatically saved to: `{saved_path}`")

            except Exception as e:
                logger.error(f"UI error: {e}")
                st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
