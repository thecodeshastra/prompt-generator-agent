"""Memory manager for prompt engineering notes."""

# Standard library imports
import os
import re
from typing import List, Dict, Any

# Third-party imports

# Local imports
from core.utils.logger import logger


class MemoryManager:
    """
    Manages loading and querying prompt engineering notes from Markdown.

    This class loads notes from a Markdown file and provides methods to retrieve
    relevant notes based on keywords or topics.
    """

    def __init__(self, memory_file: str = "prompt_engineering_notes.md"):
        """
        Initialize the memory manager.

        Args:
            memory_file (str): Path to the Markdown file containing notes.
        """
        self.memory_file = os.path.join(os.path.dirname(__file__), memory_file)
        self.notes_content = ""
        self.sections: List[Dict[str, str]] = []
        self._load_notes()

    def _load_notes(self) -> None:
        """
        Load notes from the Markdown file and parse into sections.

        If the file doesn't exist, log a warning and continue with empty notes.
        """
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.notes_content = f.read().strip()
                self._parse_sections()
                logger.info(
                    f"Loaded notes from memory ({len(self.sections)} sections)."
                )
            except IOError as e:
                logger.error(f"Failed to load memory notes: {e}")
        else:
            logger.warning(
                f"Memory file {self.memory_file} not found. Using empty memory."
            )

    def _parse_sections(self) -> None:
        """
        Parse the markdown content into sections based on headers.
        """
        # Split by headers (lines starting with #)
        header_pattern = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
        parts = header_pattern.split(self.notes_content)
        self.sections = []

        # Process parts: [before_first, header1, content1, header2, content2, ...]
        for i in range(1, len(parts), 2):
            header = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            self.sections.append({"header": header, "content": content})

    def get_relevant_notes(self, query: str, max_chars: int = 1000) -> str:
        """
        Retrieve relevant notes based on a query.

        Searches sections for matching keywords.

        Args:
            query (str): The query string to match against notes.
            max_chars (int): Maximum characters to return.

        Returns:
            str: Relevant notes excerpt.
        """
        if not self.sections:
            return ""

        query_lower = query.lower()
        relevant_sections = []

        for section in self.sections:
            header_lower = section["header"].lower()
            content_lower = section["content"].lower()

            # Check if query matches header or content
            if query_lower in header_lower or any(
                word in content_lower for word in query_lower.split()
            ):
                relevant_sections.append(section)

        if relevant_sections:
            # Combine relevant sections, limited to max_chars
            combined = "\n\n".join(
                f"## {sec['header']}\n{sec['content']}" for sec in relevant_sections
            )
            return combined[:max_chars].strip()
        else:
            return ""

    def get_all_notes(self) -> str:
        """
        Retrieve all notes content.

        Returns:
            str: The full notes content.
        """
        return self.notes_content
