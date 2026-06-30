# * File Manager Tool for Agent

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List


class FileManager:
    """Tools for managing local files and directories.

    All paths may be absolute or relative to the current working directory.
    """

    def __init__(self) -> None:
        """Initialize the file manager."""
        pass

    #^ ==========================================================
    #^ 1) File Related Tools
    #^ ==========================================================

    def create_file(self, file_name: str) -> str:
        """Create an empty file.

        Parent directories are created automatically.

        Args:
            file_name: File path to create.

        Returns:
            Status message.
        """
        path = Path(file_name)

        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            return f"File already exists: {path}"

        path.touch()

        return f"File created successfully: {path}"

    def read_file(self, file_name: str):
        """Read a file.

        Returns text for UTF-8 files, otherwise returns raw bytes.

        Args:
            file_name: File path.

        Returns:
            str | bytes: File contents.
        """
        path = Path(file_name)

        if not path.exists():
            raise FileNotFoundError(path)

        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_bytes()

    def write_file(self, file_name: str, content) -> str:
        """Overwrite a file.

        Creates the file if it does not exist.

        Args:
            file_name: Destination file path.
            content: Text (str) or binary (bytes) data.

        Returns:
            Status message.
        """
        path = Path(file_name)

        path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(str(content), encoding="utf-8")

        return f"Written successfully: {path}"

    def append_file(self, file_name: str, content) -> str:
        """Append data to a file.

        Creates the file if it does not exist.

        Args:
            file_name: File path.
            content: Text (str) or binary (bytes) data.

        Returns:
            Status message.
        """
        path = Path(file_name)

        path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(content, bytes):
            with open(path, "ab") as f:
                f.write(content)
        else:
            with open(path, "a", encoding="utf-8") as f:
                f.write(str(content))

        return f"Appended successfully: {path}"

    def delete_file(self, file_name: str) -> str:
        """Delete a file.

        Args:
            file_name: File path.

        Returns:
            Status message.
        """
        path = Path(file_name)

        if not path.exists():
            raise FileNotFoundError(path)

        if not path.is_file():
            raise IsADirectoryError(path)

        path.unlink()

        return f"Deleted file: {path}"

    #^ ==========================================================
    #^ 2) Directory Related Tools
    #^ ==========================================================

    def create_directory(self, path: str, name: str) -> str:
        """Create a directory.

        Parent directories are created automatically.

        Args:
            path: Parent directory.
            name: Name of the new directory.

        Returns:
            Status message.
        """
        directory = Path(path) / name

        directory.mkdir(parents=True, exist_ok=True)

        return f"Directory created: {directory}"

    def delete_directory(self, path: str) -> str:
        """Delete a directory recursively.

        Args:
            path: Directory path.

        Returns:
            Status message.
        """
        directory = Path(path)

        if not directory.exists():
            raise FileNotFoundError(directory)

        if not directory.is_dir():
            raise NotADirectoryError(directory)

        shutil.rmtree(directory)

        return f"Directory deleted: {directory}"

    #^ ==========================================================
    #^ 3) Other File & Directory Operations
    #^ ==========================================================

    def move(self, source: str, destination: str) -> str:
        """Move a file or directory.

        Args:
            source: Existing file or directory.
            destination: Destination path.

        Returns:
            Status message.
        """
        src = Path(source)
        dst = Path(destination)

        shutil.move(str(src), str(dst))

        return f"Moved '{src}' -> '{dst}'"

    def copy(self, source: str, destination: str) -> str:
        """Copy a file or directory.

        Directories are copied recursively.

        Args:
            source: Existing file or directory.
            destination: Destination path.

        Returns:
            Status message.
        """
        src = Path(source)
        dst = Path(destination)

        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

        return f"Copied '{src}' -> '{dst}'"

    def rename(self, path: str, new_name: str) -> str:
        """Rename a file or directory.

        Args:
            path: Existing file or directory.
            new_name: New name only.

        Returns:
            Status message.
        """
        src = Path(path)

        if not src.exists():
            raise FileNotFoundError(src)

        dst = src.with_name(new_name)

        src.rename(dst)

        return f"Renamed '{src}' -> '{dst}'"

    def exists(self, path: str) -> bool:
        """Check whether a file or directory exists.

        Args:
            path: File or directory path.

        Returns:
            True if the path exists, otherwise False.
        """
        return Path(path).exists()

    def list_directories(self, path: str) -> List[str]:
        """List immediate subdirectories.

        Args:
            path: Parent directory.

        Returns:
            List of directory paths.
        """
        directory = Path(path)

        if not directory.exists():
            raise FileNotFoundError(directory)

        return [str(item) for item in directory.iterdir() if item.is_dir()]

    def search(self, path: str, pattern: str = "*") -> List[str]:
        """Recursively search using a glob pattern.

        Examples:
            *.py
            *.txt
            *

        Args:
            path: Root directory.
            pattern: Glob pattern.

        Returns:
            List of matching paths.
        """
        directory = Path(path)

        if not directory.exists():
            raise FileNotFoundError(directory)

        return [str(item) for item in directory.rglob(pattern)]

    def get_metadata(self, path: str) -> Dict[str, Any]:
        """Get filesystem metadata.

        Args:
            path: File or directory path.

        Returns:
            Dictionary containing metadata.
        """
        p = Path(path)

        if not p.exists():
            raise FileNotFoundError(p)

        stat = p.stat()

        return {
            "name": p.name,
            "path": str(p.resolve()),
            "type": "directory" if p.is_dir() else "file",
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "suffix": p.suffix,
            "parent": str(p.parent),
            "absolute": str(p.absolute()),
        }

    def open_file(self, path: str) -> str:
        """Open a file using the system's default application.

        Args:
            path: File path.

        Returns:
            Status message.
        """
        file = Path(path)

        if not file.exists():
            raise FileNotFoundError(file)

        if not file.is_file():
            raise IsADirectoryError(file)

        try:
            os.startfile(file)
            return f"Opened file: {file}"
        except AttributeError:
            return "Opening files is supported only on Windows."

    def open_directory(self, path: str) -> str:
        """Open a directory in the system file explorer.

        Args:
            path: Directory path.

        Returns:
            Status message.
        """
        directory = Path(path)

        if not directory.exists():
            raise FileNotFoundError(directory)

        if not directory.is_dir():
            raise NotADirectoryError(directory)

        try:
            os.startfile(directory)
            return f"Opened directory: {directory}"
        except AttributeError:
            return "Opening directories is supported only on Windows."