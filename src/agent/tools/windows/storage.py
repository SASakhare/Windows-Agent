# * Storage Tool for Agent

import os
import shutil
from typing import Any, Dict, List, Optional

import psutil

from src.agent.tools.base_tool import BaseTool


class StorageTool(BaseTool):
    """Tool for inspecting and managing Windows storage/disk state.

    Provides methods to check disk usage, free space, enumerate
    drives, mount/unmount volumes, empty the recycle bin, and find
    the largest files on disk.
    """

    def __init__(self) -> None:
        """Initialize the storage tool."""
        pass

    @property
    def name(self) -> str:
        return "storage"

    @property
    def description(self) -> str:
        return (
            "Inspect and manage Windows disk storage: usage, drives, mounts, cleanup."
        )

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "disk_usage": self.disk_usage,
            "free_space": self.free_space,
            "drives": self.drives,
            "mount": self.mount,
            "unmount": self.unmount,
            "recycle_bin_empty": self.recycle_bin_empty,
            "largest_files": self.largest_files,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # Disk Usage
    # ==========================================================

    def disk_usage(self, path: str = "C:\\") -> Dict[str, Any]:
        """Get total, used, and free space for a given path/drive.

        Args:
            path: Path or drive root to inspect (e.g. "C:\\").

        Returns:
            Dictionary containing:
                path: The inspected path.
                total_gb: Total capacity in GB.
                used_gb: Used space in GB.
                free_gb: Free space in GB.
                percent_used: Percentage of space used.

        Raises:
            RuntimeError: If the path does not exist or is not accessible.
        """
        try:
            usage = shutil.disk_usage(path)
        except (FileNotFoundError, OSError) as exc:
            raise RuntimeError(
                f"Could not read disk usage for '{path}': {exc}"
            ) from exc

        gb = 1024**3
        return {
            "path": path,
            "total_gb": round(usage.total / gb, 2),
            "used_gb": round(usage.used / gb, 2),
            "free_gb": round(usage.free / gb, 2),
            "percent_used": (
                round((usage.used / usage.total) * 100, 2) if usage.total else 0.0
            ),
        }

    def free_space(self, path: str = "C:\\") -> float:
        """Get free space available on a given path/drive, in GB.

        Args:
            path: Path or drive root to inspect (e.g. "C:\\").

        Returns:
            Free space in gigabytes.

        Raises:
            RuntimeError: If the path does not exist or is not accessible.
        """
        try:
            usage = shutil.disk_usage(path)
        except (FileNotFoundError, OSError) as exc:
            raise RuntimeError(
                f"Could not read free space for '{path}': {exc}"
            ) from exc

        return round(usage.free / (1024**3), 2)

    # ==========================================================
    # Drives / Partitions
    # ==========================================================

    def drives(self, all_partitions: bool = False) -> List[Dict[str, Any]]:
        """Enumerate mounted drives/partitions and their usage.

        Args:
            all_partitions: If True, include non-physical/pseudo
                partitions as well (passed to psutil).

        Returns:
            List of dictionaries. Each dictionary contains:
                device: Device identifier (e.g. "C:\\").
                mountpoint: Mount point path.
                fstype: Filesystem type (e.g. "NTFS").
                opts: Mount options string.
                total_gb: Total capacity in GB.
                used_gb: Used space in GB.
                free_gb: Free space in GB.
                percent_used: Percentage of space used.
        """
        partitions = psutil.disk_partitions(all=all_partitions)
        gb = 1024**3

        result: List[Dict[str, Any]] = []

        for part in partitions:
            entry: Dict[str, Any] = {
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "opts": part.opts,
                "total_gb": None,
                "used_gb": None,
                "free_gb": None,
                "percent_used": None,
            }

            try:
                usage = psutil.disk_usage(part.mountpoint)
                entry["total_gb"] = round(usage.total / gb, 2)
                entry["used_gb"] = round(usage.used / gb, 2)
                entry["free_gb"] = round(usage.free / gb, 2)
                entry["percent_used"] = usage.percent
            except (PermissionError, OSError):
                # Unreadable media (e.g. empty CD/DVD drive) - leave usage as None.
                pass

            result.append(entry)

        return result

    # ==========================================================
    # Mount / Unmount
    # ==========================================================

    def mount(self, drive_letter: str, volume_path: str) -> str:
        """Mount a volume to a drive letter.

        Args:
            drive_letter: Target drive letter, e.g. "E:".
            volume_path: Path to the volume to mount, e.g.
                "\\\\?\\Volume{guid}\\".

        Returns:
            Status message.

        Raises:
            RuntimeError: If the mount command fails.
        """
        import subprocess

        result = subprocess.run(
            ["mountvol", drive_letter, volume_path],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to mount '{volume_path}' to '{drive_letter}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return f"Mounted '{volume_path}' to '{drive_letter}'."

    def unmount(self, drive_letter: str) -> str:
        """Unmount (remove) a drive letter's volume assignment.

        Args:
            drive_letter: Drive letter to unmount, e.g. "E:".

        Returns:
            Status message.

        Raises:
            RuntimeError: If the unmount command fails.
        """
        import subprocess

        result = subprocess.run(
            ["mountvol", drive_letter, "/D"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to unmount '{drive_letter}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return f"Unmounted '{drive_letter}'."

    # ==========================================================
    # Cleanup
    # ==========================================================

    def recycle_bin_empty(self, confirm: bool = False) -> str:
        """Empty the Windows Recycle Bin.

        This is a destructive, irreversible action. The caller must
        pass confirm=True; otherwise the action is refused so the
        agent cannot empty the recycle bin by accident.

        Args:
            confirm: Must be explicitly True to proceed.

        Returns:
            Status message.

        Raises:
            ValueError: If confirm is not True.
            RuntimeError: If the operation fails.
        """
        if not confirm:
            raise ValueError(
                "Refusing to empty the Recycle Bin without confirm=True. "
                "This action is irreversible."
            )

        try:
            import winshell  # type: ignore

            winshell.recycle_bin().empty(
                confirm=confirm, show_progress=False, sound=False
            )
        except ImportError:
            # Fallback via PowerShell if winshell isn't installed.
            import subprocess

            result = subprocess.run(
                ["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction Stop"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"Failed to empty Recycle Bin: "
                    f"{result.stderr.strip() or result.stdout.strip()}"
                )
        except Exception as exc:
            raise RuntimeError(f"Failed to empty Recycle Bin: {exc}") from exc

        return "Recycle Bin emptied."

    # ==========================================================
    # Analysis
    # ==========================================================

    def largest_files(
        self,
        path: str = "C:\\",
        top_n: int = 10,
        min_size_mb: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """Find the largest files under a given path.

        Args:
            path: Root directory to search.
            top_n: Maximum number of files to return.
            min_size_mb: Skip files smaller than this size, in MB.

        Returns:
            List of dictionaries, sorted largest first. Each contains:
                path: Full file path.
                size_mb: File size in MB.

        Raises:
            RuntimeError: If the path does not exist.
        """
        if not os.path.isdir(path):
            raise RuntimeError(f"Path does not exist or is not a directory: '{path}'")

        min_size_bytes = min_size_mb * 1024 * 1024
        matches: List[Dict[str, Any]] = []

        for root, _dirs, files in os.walk(path, onerror=lambda e: None):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    size = os.path.getsize(fpath)
                except OSError:
                    continue

                if size >= min_size_bytes:
                    matches.append(
                        {"path": fpath, "size_mb": round(size / (1024 * 1024), 2)}
                    )

        matches.sort(key=lambda item: item["size_mb"], reverse=True)
        return matches[:top_n]


if __name__ == "__main__":
    tool = StorageTool()

    print("=== Disk Usage (C:\\) ===")
    print(tool.disk_usage())

    print("\n=== Free Space (C:\\) ===")
    print(tool.free_space())

    print("\n=== Drives ===")
    print(tool.drives())

    # print("\n=== Largest Files ===")
    # print(tool.largest_files(path="C:\\Users", top_n=5))
    print("\n=== Recycle Bin Empty (confirm=False) ===")
    print(tool.recycle_bin_empty(confirm=True))
