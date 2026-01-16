"""Command-line interface for the prompt generator agent."""

# standard library imports
import os
import sys

# third party imports
from dotenv import load_dotenv

# prompt generator imports
from agent.orchestrator import PromptGeneratorOrchestrator
from core.utils.exporter import save_result_to_markdown
from core.utils.logger import logger

# load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def main():
    """
    Main CLI function.

    Runs an interactive loop to get user input and display pipeline results.
    """
    print("Prompt Generator Agent CLI")
    print("=" * 40)

    try:
        orchestrator = PromptGeneratorOrchestrator()
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return

    while True:
        try:
            user_input = input(
                "\nDescribe the prompt you want to generate (or 'exit' to quit): "
            ).strip()

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not user_input:
                print("Please enter a description.")
                continue

            print("\nProcessing...")
            result = orchestrator.run_pipeline(user_input)

            # Display iteration status but not full results
            if result.get("error"):
                print(f"\n❌ ERROR: {result['error']}")
            elif not result.get("generated_prompt") or result.get("generated_prompt") == "Failed to generate":
                print("\n❌ Failed to generate prompt.")
            else:
                # Save to file only on success
                saved_path = save_result_to_markdown(result, user_input)
                if saved_path:
                    print(f"\n📁 Result saved to: {saved_path}")
                
                # Still show if not approved but successfully generated
                review = result.get("review", {})
                if not review.get("approved"):
                    print(f"⚠️ Note: Prompt was not approved (Rating: {review.get('rating', 'N/A')}/5)")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
