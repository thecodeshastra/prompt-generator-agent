import sys
import os

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from agent.memory.memory_manager import MemoryManager


def test_memory_loading():
    print("Testing MemoryManager loading...")

    # Initialize MemoryManager (should load both default files)
    memory = MemoryManager()

    # Check if content from both files is present
    all_notes = memory.get_all_notes()

    # Check for building_custom_gpt.md content
    expected_gpt_phrase = "Building a Custom GPT"
    if expected_gpt_phrase in all_notes:
        print(f"PASS: Found '{expected_gpt_phrase}' in memory.")
    else:
        print(f"FAIL: Did not find '{expected_gpt_phrase}' in memory.")

    # Check sections count
    print(f"Total sections loaded: {len(memory.sections)}")

    # Debug: Print all headers
    print("Parsed Sections Headers:")
    for i, sec in enumerate(memory.sections):
        print(f"{i}: {sec['header']}")

    # Test retrieval
    query = "persona"
    relevant = memory.get_relevant_notes(query)
    if relevant:
        print(f"PASS: Retrieved relevant notes for '{query}'.")
        # print(f"Excerpt: {relevant[:100]}...")
    else:
        print(f"FAIL: No relevant notes found for '{query}'.")

    # Test retrieval from new file specifically
    # "Lexicography" is written as "**L**exicography" in the file, so it won't match "lexicography" contiguously.
    # "Cognitive Verifiers" is a better unique string.
    query_new = "Cognitive Verifiers"
    # Increase max_chars to avoid truncation if multiple sections match partial words
    relevant_new = memory.get_relevant_notes(query_new, max_chars=5000)
    print(f"Query: '{query_new}' returned {len(relevant_new)} chars.")
    if "Cognitive Verifiers" in relevant_new:
        print(f"PASS: Retrieved relevant notes for '{query_new}' from new file.")
    else:
        print(f"FAIL: No relevant notes found for '{query_new}' from new file.")
        print(f"Returned content (first 500 chars):\n{relevant_new[:500]}")

    # Another test with multi-word
    query_pattern = "Flipped Interaction Pattern"
    relevant_pattern = memory.get_relevant_notes(query_pattern, max_chars=5000)
    if "Flipped Interaction" in relevant_pattern:
        print(f"PASS: Retrieved relevant notes for 'Flipped Interaction'.")
    else:
        print(f"FAIL: Did not retrieve 'Flipped Interaction'.")
        print(f"Returned content (first 500 chars):\n{relevant_pattern[:500]}")


if __name__ == "__main__":
    test_memory_loading()
