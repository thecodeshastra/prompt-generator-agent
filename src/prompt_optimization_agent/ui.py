"""Streamlit UI for the prompt optimization agent."""

import json

import streamlit as st

from prompt_optimization_agent.agent.orchestrator import PromptOptimizationOrchestrator
from prompt_optimization_agent.core.config.input_config import PromptMode
from prompt_optimization_agent.core.utils.logger import logger


def main():
    """Main Streamlit app function."""
    st.title("Prompt Optimization Agent")
    st.markdown("Optimize, review, harden, and test prompts with AI assistance.")

    st.sidebar.header("Configuration")

    mode = st.sidebar.selectbox(
        "Output Mode",
        options=[
            PromptMode.GENERAL_LLM,
            PromptMode.CUSTOM_GPT,
            PromptMode.AGENT,
            PromptMode.JSON,
            PromptMode.ACTION_SCHEMA,
        ],
        format_func=lambda x: {
            PromptMode.GENERAL_LLM: "General LLM",
            PromptMode.CUSTOM_GPT: "Custom GPT",
            PromptMode.AGENT: "AI Agent",
            PromptMode.JSON: "JSON Output",
            PromptMode.ACTION_SCHEMA: "OpenAPI Action Schema",
        }[x],
        index=0,
    )

    output_format = st.sidebar.radio("Output Format", ["markdown", "json"], horizontal=True)

    if "orchestrator" not in st.session_state or st.session_state.get("current_mode") != mode:
        try:
            st.session_state.orchestrator = PromptOptimizationOrchestrator(mode=mode)
            st.session_state.current_mode = mode
        except Exception as e:
            st.error(f"Failed to initialize: {e}")
            return

    st.header("Step 1: Describe Your Prompt")
    user_input = st.text_area(
        "Enter a description of the prompt you want to optimize:",
        height=100,
        placeholder="e.g., A prompt for summarizing meeting notes with action items",
    )

    if st.button("Optimize Prompt", type="primary"):
        if not user_input.strip():
            st.error("Please enter a description.")
        else:
            status_container = st.status("Processing Pipeline...", expanded=True)

            def update_log(message):
                if "logs" not in st.session_state:
                    st.session_state.logs = []
                st.session_state.logs.append(message)
                status_container.write(message)

            try:
                st.session_state.logs = []
                orchestrator = st.session_state.orchestrator

                result = orchestrator.run_pipeline(
                    user_input,
                    mode=mode,
                    output_format=output_format,
                    status_callback=update_log,
                )

                status_container.update(label="Pipeline Completed!", state="complete", expanded=False)
                st.session_state.result = result

            except Exception as e:
                logger.error(f"UI error: {e}")
                st.error(f"An error occurred: {e}")
                status_container.update(label="Pipeline Failed", state="error")
                st.session_state.result = None

    if "result" in st.session_state and st.session_state.result:
        result = st.session_state.result
        st.divider()
        st.header("Final Result")

        if result.get("error"):
            st.error(f"Pipeline Error: {result['error']}")
            return

        generated_prompt = result.get("hardened_prompt", result.get("generated_prompt", "Failed to optimize"))

        st.subheader("🚀 Optimized Prompt")
        st.caption("Copy the optimized prompt below:")

        if output_format == "json":
            st.json({"prompt": generated_prompt})
        else:
            st.code(generated_prompt, language="markdown")

        col1, col2, col3 = st.columns(3)
        with col1:
            review = result.get("review", {})
            approved = review.get("approved", False)
            if approved:
                st.success("Verdict: Approved")
            else:
                st.error("Verdict: Rejected")
        with col2:
            st.metric("Quality Rating", f"{review.get('rating', 'N/A')}/5")
        with col3:
            if result.get("risk_analysis") and not result.get("risk_analysis", {}).get("error"):
                risk = result["risk_analysis"]
                st.metric("Risk Score", f"{risk.get('overall_risk_score', 'N/A')}/10")

        if review.get("feedback"):
            st.info(f"**Reviewer Feedback:** {review.get('feedback')}")

        if result.get("risk_analysis") and not result.get("risk_analysis", {}).get("error"):
            with st.expander("📊 Risk Analysis"):
                risk = result["risk_analysis"]
                st.markdown(f"**Risk Level:** {risk.get('risk_level', 'unknown').upper()}")
                if risk.get("risks"):
                    for r in risk["risks"][:5]:
                        st.markdown(
                            f"- **{r.get('category')}** ({r.get('severity')}): {r.get('description')}"
                        )

        if result.get("metadata"):
            with st.expander("📋 Metadata"):
                meta = result["metadata"]
                st.markdown(f"- **Version:** {meta.get('version')}")
                st.markdown(f"- **Mode:** {meta.get('mode')}")
                st.markdown(f"- **Complexity:** {meta.get('complexity_level')}")
                st.markdown(f"- **Created:** {meta.get('created_at')}")

        if result.get("test_cases"):
            st.subheader("🧪 Validation Test Cases")
            test_cases = result.get("test_cases")
            if test_cases:
                for i, tc in enumerate(test_cases, 1):
                    with st.expander(f"Test Case {i}: {tc.get('input', 'N/A')[:50]}..."):
                        st.markdown(f"**Input:**\n{tc.get('input', 'N/A')}")
                        st.markdown(f"**Expected Output:**\n{tc.get('expected_output', 'N/A')}")
                        if tc.get("rubric"):
                            st.markdown(f"**Rubric:** {tc.get('rubric')}")
            else:
                st.info("No test cases generated.")

    if "logs" in st.session_state and st.session_state.logs:
        with st.expander("Show Full Pipeline Logs", expanded=False):
            st.code("\n".join(st.session_state.logs), language="text")


if __name__ == "__main__":
    main()
