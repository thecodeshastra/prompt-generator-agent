"""Command-line interface for the prompt optimization agent."""

import json

from dotenv import load_dotenv

from prompt_optimization_agent.agent.orchestrator import PromptOptimizationOrchestrator
from prompt_optimization_agent.core.config.input_config import PromptMode
from prompt_optimization_agent.core.utils.exporter import save_result_to_markdown
from prompt_optimization_agent.core.utils.logger import logger

load_dotenv()

MODES = {
    "1": ("general_llm", "General LLM (ChatGPT, Claude, etc.)"),
    "2": ("custom_gpt", "Custom GPT (GPT Builder)"),
    "3": ("agent", "AI Agent System Prompt"),
    "4": ("json", "JSON Output (API/Automation)"),
    "5": ("action_schema", "OpenAPI Action Schema"),
}


def print_menu():
    """Print the mode selection menu."""
    print("\nSelect output mode:")
    for key, (mode, desc) in MODES.items():
        print(f"  {key}. {desc}")
    print("  0. Skip (use default: General LLM)")


def get_mode_choice() -> PromptMode:
    """Get mode choice from user."""
    print_menu()
    choice = input("\nEnter mode (0-5): ").strip()
    if choice in MODES:
        return PromptMode(MODES[choice][0])
    return PromptMode.GENERAL_LLM


def main():
    """Main CLI function."""
    print("=" * 50)
    print("   Prompt Optimization Agent CLI")
    print("=" * 50)

    mode = get_mode_choice()
    print(f"\n✓ Using mode: {mode.value}")

    try:
        orchestrator = PromptOptimizationOrchestrator(mode=mode)
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    while True:
        try:
            user_input = input(
                "\nDescribe the idea you want to optimize into a prompt (or 'exit' to quit): "
            ).strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter a description.")
                continue

            output_format = input("Output format? (m)arkdown or (j)son [default: m]: ").strip().lower()
            use_json = output_format == "j"

            print("\nProcessing...")
            result = orchestrator.run_pipeline(user_input, output_format="json" if use_json else "markdown")

            if result.get("error"):
                print(f"\n❌ ERROR: {result['error']}")
            elif not result.get("generated_prompt"):
                print("\n❌ Failed to optimize prompt.")
            else:
                if use_json:
                    print("\n" + "=" * 40)
                    print("OPTIMIZED PROMPT (JSON):")
                    print("=" * 40)
                    output = {
                        "prompt": result.get("hardened_prompt", result.get("generated_prompt")),
                        "metadata": result.get("metadata", {}),
                        "risk_analysis": result.get("risk_analysis", {}),
                    }
                    print(json.dumps(output, indent=2))
                else:
                    print("\n" + "=" * 40)
                    print("OPTIMIZED PROMPT:")
                    print("=" * 40)
                    print(result.get("hardened_prompt", result.get("generated_prompt")))

                    saved_path = save_result_to_markdown(result, user_input)
                    if saved_path:
                        print(f"\n📁 Result saved to: {saved_path}")

                review = result.get("review", {})
                if not review.get("approved"):
                    print(f"\n⚠️ Note: Prompt was not approved (Rating: {review.get('rating', 'N/A')}/5)")

                if result.get("risk_analysis") and not result.get("risk_analysis", {}).get("error"):
                    risk = result["risk_analysis"]
                    print(
                        f"\n📊 Risk Score: {risk.get('overall_risk_score', 'N/A')}/10 ({risk.get('risk_level', 'unknown')})"
                    )

                if result.get("metadata"):
                    meta = result["metadata"]
                    print(
                        f"\n📋 Version: {meta.get('version')}, Mode: {meta.get('mode')}, Complexity: {meta.get('complexity_level')}"
                    )

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
