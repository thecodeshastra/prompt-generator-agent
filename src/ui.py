"""Streamlit UI for the prompt generator agent."""

import os
import sys

import streamlit as st

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from agent.orchestrator import PromptGeneratorOrchestrator
from core.utils.logger import logger


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
        else:
            # Status and Log containers
            status_container = st.status("Processing Pipeline...", expanded=True)
            
            def update_log(message):
                if "logs" not in st.session_state:
                    st.session_state.logs = []
                st.session_state.logs.append(message)
                status_container.write(message)

            try:
                st.session_state.logs = [] # Reset logs
                orchestrator = st.session_state.orchestrator
                
                # Run pipeline with callback
                result = orchestrator.run_pipeline(user_input, status_callback=update_log)

                status_container.update(label="Pipeline Completed!", state="complete", expanded=False)

                # Store result in session
                st.session_state.result = result

            except Exception as e:
                logger.error(f"UI error: {e}")
                st.error(f"An error occurred: {e}")
                status_container.update(label="Pipeline Failed", state="error")
                st.session_state.result = None

    # --- DISPLAY RESULTS (Persistently) ---
    if "result" in st.session_state and st.session_state.result:
        result = st.session_state.result
        st.divider()
        st.header("Final Result")
        
        generated_prompt = result.get("generated_prompt", "Failed to generate")
        
        # Output Box for Copying
        st.subheader("🚀 Generated Prompt")
        st.caption("Copy the generated prompt below:")
        st.code(generated_prompt, language="markdown")

        # Review Details in Columns
        st.subheader("📋 Review Audit")
        review = result.get("review", {})
        approved = review.get("approved", False)
        
        col1, col2 = st.columns(2)
        with col1:
            if approved:
                st.success("Verdict: Approved")
            else:
                st.error("Verdict: Rejected")
        with col2:
            st.metric("Quality Rating", f"{review.get('rating', 'N/A')}/5")

        st.info(f"**Reviewer Feedback:** {review.get('feedback', 'No feedback provided.')}")

        # Test cases
        st.subheader("🧪 Validation Test Cases")
        test_cases = result.get("test_cases")
        
        if approved:
            if test_cases:
                for i, tc in enumerate(test_cases, 1):
                    with st.expander(f"Test Case {i}: {tc.get('input', 'N/A')[:50]}..."):
                        st.markdown(f"**Input:**\n{tc.get('input', 'N/A')}")
                        st.markdown(f"**Expected Output:**\n{tc.get('expected_output', 'N/A')}")
                        if tc.get('rubric'):
                            st.markdown(f"**Rubric:** {tc.get('rubric')}")
            elif test_cases == []:
                error_msg = result.get("test_error", "Unknown error in test generation.")
                st.error(f"Failed to generate test cases: {error_msg}")
            else:
                st.info("Test cases were skipped.")
        else:
            st.warning("Test cases skipped (Prompt not approved).")

        if "error" in result:
            st.error(f"Pipeline Error: {result['error']}")

    # Persistent log view at the bottom if logs exist
    if "logs" in st.session_state and st.session_state.logs:
        with st.expander("Show Full Pipeline Logs", expanded=False):
            st.code("\n".join(st.session_state.logs), language="text")


if __name__ == "__main__":
    main()
