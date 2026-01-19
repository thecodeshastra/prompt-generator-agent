"""Memory manager for prompt engineering notes."""

# Standard library imports
import os
import re
from typing import Dict, List

# Third-party imports
# Local imports
from core.utils.logger import logger


class MemoryManager:
    """
    Manages loading and querying prompt engineering notes from Markdown.

    This class loads notes from a Markdown file and provides methods to retrieve
    relevant notes based on keywords or topics.
    """

    def __init__(
        self,
        memory_files: List[str] = None,
    ):
        """
        Initialize the memory manager.

        Args:
            memory_files (List[str]): List of filenames for the Markdown memory files.
                                      Defaults to ["prompt_engineering_notes.md", "building_custom_gpt.md"].
        """
        if memory_files is None:
            memory_files = ["prompt_engineering_notes.md", "building_custom_gpt.md"]

        self.memory_files = [os.path.join(os.path.dirname(__file__), f) for f in memory_files]
        self.notes_content = ""
        self.sections: List[Dict[str, str]] = []
        self._load_notes()

    def _load_notes(self) -> None:
        """
        Load notes from the Markdown files and parse into sections.
        """
        loaded_count = 0
        all_content = []

        for file_path in self.memory_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read().strip()
                        if file_content:
                            all_content.append(file_content)
                            loaded_count += 1
                except IOError as e:
                    logger.error(f"Failed to load memory file {file_path}: {e}")
            else:
                logger.warning(f"Memory file {file_path} not found. Skipping.")

        if all_content:
            self.notes_content = "\n\n".join(all_content)
            self._parse_sections()
            logger.info(f"Loaded notes from {loaded_count} files ({len(self.sections)} sections).")
        else:
            logger.warning("No memory files loaded. Using empty memory.")

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
            if query_lower in header_lower or any(word in content_lower for word in query_lower.split()):
                relevant_sections.append(section)

        if relevant_sections:
            # Combine relevant sections, limited to max_chars
            combined = "\n\n".join(f"## {sec['header']}\n{sec['content']}" for sec in relevant_sections)
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
