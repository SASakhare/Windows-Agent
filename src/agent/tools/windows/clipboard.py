# * Clipboard Tool for Agent

import pyperclip
from pathlib import Path
from typing import Any

from src.agent.tools.base_tool import BaseTool


class ClipboardTool(BaseTool):
    """Tools for interacting with the system clipboard."""

    def __init__(self) -> None:
        """Initialize the clipboard tool."""
        pass

    @property
    def name(self) -> str:
        return "clipboard"

    @property
    def description(self) -> str:
        return "Read, write, and manipulate the system clipboard."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "get_text": self.get_text,
            "set_text": self.set_text,
            "clear": self.clear,
            "append": self.append,
            "copy_file": self.copy_file,
            "paste": self.paste,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # 1) Clipboard Text Operations
    # ==========================================================

    def get_text(self) -> str:
        """Return the current clipboard text.

        Returns:
            Clipboard text.
        """
        return pyperclip.paste()

    def set_text(self, text: str) -> str:
        """Replace the clipboard contents.

        Args:
            text: Text to copy.

        Returns:
            Status message.
        """
        pyperclip.copy(text)
        return "Clipboard updated successfully."

    def clear(self) -> str:
        """Clear the clipboard.

        Returns:
            Status message.
        """
        pyperclip.copy("")
        return "Clipboard cleared."

    def append(self, text: str) -> str:
        """Append text to the existing clipboard contents.

        Args:
            text: Text to append.

        Returns:
            Status message.
        """
        current = pyperclip.paste()
        pyperclip.copy(current + text)
        return "Text appended to clipboard."

    # ==========================================================
    # 2) File Operations
    # ==========================================================

    def copy_file(self, file_name: str) -> str:
        """Copy a file's contents to the clipboard.

        Text files are copied as text. Binary files are not supported.

        Args:
            file_name: Path to the file.

        Returns:
            Status message.
        """
        path = Path(file_name)

        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise IsADirectoryError(path)

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Only UTF-8 text files can be copied.") from exc

        pyperclip.copy(content)
        return f"Copied '{path}' to clipboard."

    def paste(self) -> str:
        """Return the current clipboard contents.

        Returns:
            Clipboard text.
        """
        return pyperclip.paste()
    
    