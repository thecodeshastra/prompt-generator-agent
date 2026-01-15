"""Command-line interface for the prompt generator agent."""

# standard library imports
import sys
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# prompt generator imports
from agent.orchestrator import PromptGeneratorOrchestrator
from core.utils.logger import logger
from core.utils.exporter import save_result_to_markdown


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

            # Display history if iterative
            if "history" in result and len(result["history"]) > 1:
                print("\n" + "=" * 50)
                print("ITERATION HISTORY:")
                for item in result["history"]:
                    print(f"\nIteration {item['iteration']}:")
                    print(f"Generated Prompt: {item['generated_prompt'][:100]}...")
                    print(f"Review Approved: {item['review']['approved']}")
                    print(f"Rating: {item['review']['rating']}/5")
                    print(f"Feedback: {item['review']['feedback']}")

            # Display final results
            print("\n" + "=" * 50)
            print("FINAL GENERATED PROMPT:")
            print(result.get("generated_prompt", "Failed to generate"))

            print("\nFINAL REVIEW:")
            review = result.get("review", {})
            print(f"Approved: {review.get('approved', False)}")
            print(f"Rating: {review.get('rating', 'N/A')}/5")
            print(f"Feedback: {review.get('feedback', 'N/A')}")

            test_cases = result.get("test_cases")
            if test_cases:
                print("\nTEST CASES:")
                for i, tc in enumerate(test_cases, 1):
                    print(f"{i}. Input: {tc.get('input', 'N/A')}")
                    print(f"   Expected: {tc.get('expected_output', 'N/A')}")
            elif test_cases == [] and review.get("approved"):
                print("\nERROR: Failed to generate test cases.")
                if "test_error" in result:
                    print(f"Reason: {result['test_error']}")
            else:
                print("\nNo test cases generated (prompt not approved or skipped).")

            if "error" in result:
                print(f"\nERROR: {result['error']}")

            # Save to file
            saved_path = save_result_to_markdown(result, user_input)
            if saved_path:
                print(f"\n📁 Result saved to: {saved_path}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"CLI error: {e}")
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
