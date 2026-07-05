# tools/code/code_tool.py
import ast
import fnmatch
import os
import subprocess
from typing import Any, Dict, List, Optional

from src.agent.tools.base_tool import BaseTool


DEFAULT_EXCLUDES = [
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "*.pyc", ".pytest_cache", "dist", "build", ".mypy_cache",".env"
]


class CodeTool(BaseTool):
    """Read, search, edit, refactor, lint, format, and test code in a
    project directory. Designed for an LLM to work like an editor:
    understand project structure, find symbols, make precise edits,
    and verify changes via lint/tests.
    """

    def __init__(self, project_root: str = ".") -> None:
        self.project_root = os.path.abspath(project_root)

    @property
    def name(self) -> str:
        return "code"

    @property
    def description(self) -> str:
        return "Read, search, edit, refactor, lint, format, and test code in the project."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "read_project": self.read_project,
            "find_symbol": self.find_symbol,
            "replace": self.replace,
            "refactor": self.refactor,
            "lint": self.lint,
            "format": self.format,
            "run_tests": self.run_tests,
        }
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")
        return actions[action](**kwargs)

    # ==========================================================
    # Project reading
    # ==========================================================

    def read_project(
        self,
        subpath: str = ".",
        include_content: bool = False,
        max_file_size_kb: int = 50,
        extensions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Walk the project and return its file tree, optionally with contents.

        Args:
            subpath: Directory (relative to project root) to read. Use "." for the whole project.
            include_content: If True, include file contents (skips files over max_file_size_kb).
            max_file_size_kb: Skip reading content of files larger than this, in KB.
            extensions: Only include files with these extensions, e.g. [".py", ".ts"]. None = all.

        Returns:
            Dictionary with "root" and "files": a list of {path, size_bytes, content?}.

        Raises:
            RuntimeError: If subpath doesn't exist under the project root.
        """
        target = self._resolve(subpath)
        if not os.path.isdir(target):
            raise RuntimeError(f"Not a directory: '{subpath}'")

        files: List[Dict[str, Any]] = []

        for root, dirs, filenames in os.walk(target):
            dirs[:] = [d for d in dirs if not self._is_excluded(d)]

            for fname in filenames:
                if self._is_excluded(fname):
                    continue
                if extensions and not any(fname.endswith(ext) for ext in extensions):
                    continue

                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, self.project_root)

                try:
                    size = os.path.getsize(fpath)
                except OSError:
                    continue

                entry: Dict[str, Any] = {"path": rel_path, "size_bytes": size}

                if include_content and size <= max_file_size_kb * 1024:
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            entry["content"] = f.read()
                    except OSError:
                        entry["content"] = None

                files.append(entry)

        return {"root": os.path.relpath(target, self.project_root) or ".", "files": files}

    def _is_excluded(self, name: str) -> bool:
        return any(fnmatch.fnmatch(name, pattern) for pattern in DEFAULT_EXCLUDES)

    def _resolve(self, path: str) -> str:
        full = os.path.abspath(os.path.join(self.project_root, path))
        if not full.startswith(self.project_root):
            raise ValueError(f"Path '{path}' escapes the project root.")
        return full

    # ==========================================================
    # Symbol search
    # ==========================================================

    def find_symbol(self, symbol: str, extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Find where a function, class, or variable is defined across
        the project (Python files only, via AST).

        Args:
            symbol: Name of the function/class/variable to find.
            extensions: File extensions to search. Defaults to [".py"].

        Returns:
            List of dictionaries: {path, line, type ("function"/"class"/"assignment"), name}.
        """
        extensions = extensions or [".py"]
        matches: List[Dict[str, Any]] = []

        for root, dirs, filenames in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not self._is_excluded(d)]
            for fname in filenames:
                if not any(fname.endswith(ext) for ext in extensions):
                    continue

                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, self.project_root)

                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        source = f.read()
                    tree = ast.parse(source, filename=fpath)
                except (SyntaxError, OSError):
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == symbol:
                        matches.append({"path": rel_path, "line": node.lineno, "type": "function", "name": symbol})
                    elif isinstance(node, ast.ClassDef) and node.name == symbol:
                        matches.append({"path": rel_path, "line": node.lineno, "type": "class", "name": symbol})
                    elif isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id == symbol:
                                matches.append({"path": rel_path, "line": node.lineno, "type": "assignment", "name": symbol})

        return matches

    # ==========================================================
    # Editing
    # ==========================================================

    def replace(self, path: str, old_str: str, new_str: str) -> str:
        """Replace an exact, unique string in a file with another string.

        Args:
            path: File path relative to project root.
            old_str: Exact string to find (must appear exactly once).
            new_str: String to replace it with.

        Returns:
            Status message.

        Raises:
            RuntimeError: If the file doesn't exist, old_str isn't found,
                or old_str appears more than once (ambiguous).
        """
        full_path = self._resolve(path)
        if not os.path.isfile(full_path):
            raise RuntimeError(f"File not found: '{path}'")

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        count = content.count(old_str)
        if count == 0:
            raise RuntimeError(f"String not found in '{path}'.")
        if count > 1:
            raise RuntimeError(f"String appears {count} times in '{path}'; must be unique. Add more context.")

        content = content.replace(old_str, new_str, 1)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Replaced content in '{path}'."

    # ==========================================================
    # Refactoring (project-wide, structural)
    # ==========================================================

    def refactor(self, action: str, symbol: str, new_name: Optional[str] = None, path: Optional[str] = None) -> str:
        """Perform a structural refactor across the project using rope.

        Args:
            action: "rename" (rename a symbol project-wide).
            symbol: Current name of the function/class/variable to refactor.
            new_name: New name (required for "rename").
            path: File where the symbol is defined, relative to project root
                (required — rope needs a starting point to locate the symbol).

        Returns:
            Status message describing what changed.

        Raises:
            ValueError: If required arguments are missing.
            RuntimeError: If the refactor fails (symbol not found, etc.).
        """
        from rope.base.project import Project
        from rope.refactor.rename import Rename

        if action != "rename":
            raise ValueError(f"Unsupported refactor action: '{action}'. Only 'rename' is supported.")
        if not new_name or not path:
            raise ValueError("refactor(action='rename') requires both 'new_name' and 'path'.")

        full_path = self._resolve(path)
        if not os.path.isfile(full_path):
            raise RuntimeError(f"File not found: '{path}'")

        with open(full_path, "r", encoding="utf-8") as f:
            source = f.read()

        offset = source.find(symbol)
        if offset == -1:
            raise RuntimeError(f"Symbol '{symbol}' not found in '{path}'.")

        project = Project(self.project_root)
        try:
            resource = project.get_resource(path)
            rename = Rename(project, resource, offset)
            changes = rename.get_changes(new_name)
            project.do(changes)
        except Exception as exc:
            raise RuntimeError(f"Refactor failed: {exc}") from exc
        finally:
            project.close()

        return f"Renamed '{symbol}' to '{new_name}' project-wide, starting from '{path}'."

    # ==========================================================
    # Lint / Format
    # ==========================================================

    def lint(self, path: str = ".") -> Dict[str, Any]:
        """Run ruff on a file or directory and return issues found.

        Args:
            path: File or directory relative to project root. Default: whole project.

        Returns:
            Dictionary with success (bool, True if no issues) and issues (list of raw ruff output lines).
        """
        target = self._resolve(path)
        result = subprocess.run(
            ["ruff", "check", target, "--output-format=concise"],
            capture_output=True, text=True, cwd=self.project_root, check=False,
        )
        issues = [line for line in result.stdout.splitlines() if line.strip()]
        return {"success": result.returncode == 0, "issues": issues}

    def format(self, path: str = ".") -> str:
        """Run black on a file or directory to auto-format code.

        Args:
            path: File or directory relative to project root. Default: whole project.

        Returns:
            Status message with black's summary output.

        Raises:
            RuntimeError: If black fails to run.
        """
        target = self._resolve(path)
        result = subprocess.run(
            ["black", target], capture_output=True, text=True, cwd=self.project_root, check=False,
        )
        if result.returncode not in (0, 1):  # black returns 1 if it reformatted files - not an error
            raise RuntimeError(f"Formatting failed: {result.stderr.strip()}")
        return result.stderr.strip() or "No changes needed."

    # ==========================================================
    # Tests
    # ==========================================================

    def run_tests(self, path: str = ".", keyword: Optional[str] = None) -> Dict[str, Any]:
        """Run pytest on the project or a specific path.

        Args:
            path: File, directory, or test node id relative to project root.
            keyword: Optional -k keyword filter to run matching tests only.

        Returns:
            Dictionary with success (bool), summary (str), and raw_output (str, truncated).
        """
        target = self._resolve(path)
        cmd = ["pytest", target, "-v"]
        if keyword:
            cmd += ["-k", keyword]

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=self.project_root, check=False,
        )
        output = result.stdout + result.stderr
        summary_lines = [l for l in output.splitlines() if "passed" in l or "failed" in l or "error" in l]
        summary = summary_lines[-1] if summary_lines else "No summary line found."

        return {
            "success": result.returncode == 0,
            "summary": summary,
            "raw_output": output[-4000:],  # cap to avoid flooding context
        }


if __name__ == "__main__":
    tool = CodeTool(project_root=".")
    print(tool.execute("read_project", subpath=".", include_content=False))
    print(tool.execute("find_symbol", symbol="CodeTool"))
    print(tool.execute("lint", path="."))