# * Power Tool for Agent

import ctypes
import subprocess
from typing import Any, Dict

import psutil

from src.agent.tools.base_tool import BaseTool


class PowerTool(BaseTool):
    """Tool for managing Windows power operations.

    Provides methods to shut down, restart, sleep, hibernate,
    lock, sign out, inspect battery information, and change
    the active Windows power plan.
    """

    def __init__(self) -> None:
        """Initialize the power tool."""
        pass

    @property
    def name(self) -> str:
        return "power"

    @property
    def description(self) -> str:
        return "Manage Windows power operations."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "shutdown": self.shutdown,
            "restart": self.restart,
            "sleep": self.sleep,
            "hibernate": self.hibernate,
            "lock": self.lock,
            "sign_out": self.sign_out,
            "battery": self.battery,
            "power_mode": self.power_mode,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # Power Operations
    # ==========================================================

    def shutdown(self, force: bool = False) -> str:
        """Shut down the computer.

        Args:
            force: If True, forcibly closes running applications.

        Returns:
            Status message.
        """
        cmd = ["shutdown", "/s", "/t", "0"]
        if force:
            cmd.append("/f")

        subprocess.Popen(cmd)

        return "System shutdown initiated."

    def restart(self, force: bool = False) -> str:
        """Restart the computer.

        Args:
            force: If True, forcibly closes running applications.

        Returns:
            Status message.
        """
        cmd = ["shutdown", "/r", "/t", "0"]
        if force:
            cmd.append("/f")

        subprocess.Popen(cmd)

        return "System restart initiated."

    def sleep(self) -> str:
        """Put the computer into sleep mode.

        Returns:
            Status message.
        """
        ctypes.windll.powrprof.SetSuspendState(False, True, False)
        return "System entering sleep mode."

    def hibernate(self) -> str:
        """Hibernate the computer.

        Returns:
            Status message.
        """
        ctypes.windll.powrprof.SetSuspendState(True, True, False)
        return "System entering hibernation."

    def lock(self) -> str:
        """Lock the current Windows session.

        Returns:
            Status message.
        """
        ctypes.windll.user32.LockWorkStation()
        return "Workstation locked."

    def sign_out(self) -> str:
        """Sign out the current Windows user.

        Returns:
            Status message.
        """
        subprocess.Popen(["shutdown", "/l"])
        return "Sign out initiated."

    # ==========================================================
    # Battery
    # ==========================================================

    def battery(self) -> Dict[str, Any]:
        """Get battery information.

        Returns:
            Dictionary containing:
                percent: Battery percentage.
                charging: Whether external power is connected.
                seconds_left: Estimated remaining battery time.
        """
        battery = psutil.sensors_battery()

        if battery is None:
            raise RuntimeError("Battery information is unavailable.")

        return {
            "percent": battery.percent,
            "charging": battery.power_plugged,
            "seconds_left": battery.secsleft,
        }

    # ==========================================================
    # Power Plans
    # ==========================================================

    def power_mode(self, mode: str) -> str:
        """Change the active Windows power plan.

        Supported modes:
            balanced
            high_performance
            power_saver

        Args:
            mode: Name of the power plan.

        Returns:
            Status message.

        Raises:
            ValueError: If an unsupported mode is supplied.
        """
        schemes = {
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a",
        }

        if mode not in schemes:
            raise ValueError(f"Unsupported power mode: {mode}")

        subprocess.run(
            ["powercfg", "/setactive", schemes[mode]],
            check=True,
        )

        return f"Power mode changed to '{mode}'."