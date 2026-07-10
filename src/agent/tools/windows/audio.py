# * Audio Tool for Agent

from typing import Any, List

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from src.agent.tools.base_tool import BaseTool


class AudioTool(BaseTool):
    """Tools for controlling the system audio."""

    def __init__(self) -> None:
        """Initialize the audio tool."""
        devices = AudioUtilities.GetSpeakers()
        self._volume = devices.EndpointVolume  # type: ignore

    @property
    def name(self) -> str:
        return "audio"

    @property
    def description(self) -> str:
        return "Control the system volume and audio devices."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "volume_up": self.volume_up,
            "volume_down": self.volume_down,
            "set_volume": self.set_volume,
            "mute": self.mute,
            "unmute": self.unmute,
            "get_volume": self.get_volume,
            "list_devices": self.list_devices,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # 1) Volume Controls
    # ==========================================================

    def volume_up(self, step: float = 10.0) -> str:
        """Increase the system volume.

        Args:
            step: Percentage to increase (0-100).

        Returns:
            Status message.
        """
        current = self.get_volume()
        self.set_volume(min(100.0, current + step))
        return f"Volume increased to {self.get_volume():.0f}%."

    def volume_down(self, step: float = 10.0) -> str:
        """Decrease the system volume.

        Args:
            step: Percentage to decrease (0-100).

        Returns:
            Status message.
        """
        current = self.get_volume()
        self.set_volume(max(0.0, current - step))
        return f"Volume decreased to {self.get_volume():.0f}%."

    def set_volume(self, level: float) -> str:
        """Set the system volume.

        Args:
            level: Volume percentage (0-100).

        Returns:
            Status message.
        """
        if not 0 <= level <= 100:
            raise ValueError("Volume must be between 0 and 100.")

        scalar = level / 100
        self._volume.SetMasterVolumeLevelScalar(scalar, None)

        return f"Volume set to {level:.0f}%."

    def mute(self) -> str:
        """Mute the system audio.

        Returns:
            Status message.
        """
        self._volume.SetMute(True, None)
        return "System muted."

    def unmute(self) -> str:
        """Unmute the system audio.

        Returns:
            Status message.
        """
        self._volume.SetMute(False, None)
        return "System unmuted."

    def get_volume(self) -> float:
        """Return the current master volume.

        Returns:
            Volume percentage.
        """
        return round(self._volume.GetMasterVolumeLevelScalar() * 100, 2)

    # ==========================================================
    # 2) Audio Devices
    # ==========================================================

    def list_devices(self) -> List[str]:
        """Return all available playback devices.

        Returns:
            List of playback device names.
        """
        return [
            device.FriendlyName
            for device in AudioUtilities.GetAllDevices()
        ]