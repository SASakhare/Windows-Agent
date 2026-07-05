# utils/admin.py

import ctypes
import sys
from typing import NoReturn


class Admin:
    """Utilities for checking and requesting administrator privileges."""

    @staticmethod
    def is_admin() -> bool:
        """Return True if the current process is running as administrator."""
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    @staticmethod
    def elevate() -> NoReturn:
        """Restart the current Python program with administrator privileges.

        Displays the Windows UAC prompt. If the user approves,
        the current process exits and an elevated copy is started.

        Raises:
            RuntimeError: If elevation could not be started or the
                user declined the UAC prompt.
        """
        params = " ".join(f'"{arg}"' for arg in sys.argv[1:])

        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            params,
            None,
            1,
        )

        # ShellExecuteW returns a value <= 32 on failure (e.g. UAC declined,
        # ERROR_FILE_NOT_FOUND, etc.)
        if result <= 32:
            raise RuntimeError(
                f"Failed to request administrator privileges (error code {result})."
            )

        sys.exit(0)

    @classmethod
    def require_admin(cls) -> None:
        """Ensure the current process is running with administrator privileges.

        Unlike a full auto-elevate, this does NOT relaunch or kill the
        current process. In a long-lived agent/tool context, silently
        exiting mid-call would kill the whole process, not just the
        current action. Instead this raises so the caller (and, in an
        agent, the user) can decide what to do next.

        Raises:
            PermissionError: If the current process is not elevated.
        """
        if not cls.is_admin():
            raise PermissionError(
                "This action requires administrator privileges. "
                "Restart the application as administrator, or call "
                "Admin.elevate() explicitly to relaunch elevated."
            )


if __name__ == "__main__":
    if Admin.is_admin():
        print("Running as administrator.")
    else:
        print("Not running as administrator. Attempting to elevate...")
        try:
            Admin.elevate()
        except RuntimeError as exc:
            print(exc)