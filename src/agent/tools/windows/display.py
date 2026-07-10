# * Display Tool for Agent

import win32api
import win32con
import pywintypes

import screen_brightness_control as sbc

from screeninfo import get_monitors
from typing import Any, Dict, List

from src.agent.tools.base_tool import BaseTool


class DisplayTool(BaseTool):
    """Tool for querying and controlling Windows display settings.

    Provides methods to retrieve monitor information, change the primary
    display resolution, adjust brightness, rotate the display, and inspect
    display scaling support.
    """

    def __init__(self) -> None:
        """Initialize the display tool."""
        pass

    @property
    def name(self) -> str:
        return "display"

    @property
    def description(self) -> str:
        return "Manage monitors and display settings."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "resolution": self.resolution,
            "change_resolution": self.change_resolution,
            "monitors": self.monitors,
            "primary_monitor": self.primary_monitor,
            "brightness": self.brightness,
            "rotate": self.rotate,
            "scale": self.scale,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # Resolution
    # ==========================================================

    def resolution(self) -> Dict[str, int]:
        """Get the current resolution of the primary display.

            Returns:
                Dictionary containing:
                    width: Screen width in pixels.
                    height: Screen height in pixels.
        """

        settings = win32api.EnumDisplaySettings(
            None,
            win32con.ENUM_CURRENT_SETTINGS,
        )

        return {
            "width": settings.PelsWidth,
            "height": settings.PelsHeight,
        }
    def change_resolution(self, width: int, height: int) -> str:
        """Change the resolution of the primary display.

        Args:
            width: Desired screen width in pixels.
            height: Desired screen height in pixels.

        Returns:
            Status message confirming the resolution change.

        Raises:
            RuntimeError: If Windows fails to change the display resolution.
        """

        devmode = pywintypes.DEVMODEType() # type: ignore
        devmode.PelsWidth = width
        devmode.PelsHeight = height
        devmode.Fields = (
            win32con.DM_PELSWIDTH |
            win32con.DM_PELSHEIGHT
        )

        result = win32api.ChangeDisplaySettings(devmode, 0)

        if result != win32con.DISP_CHANGE_SUCCESSFUL:
            raise RuntimeError("Failed to change display resolution.")

        return f"Resolution changed to {width}x{height}."

    # ==========================================================
    # Monitor Information
    # ==========================================================

    def monitors(self) -> List[Dict[str, Any]]:
        """List all connected monitors.

            Returns:
                A list of dictionaries. Each dictionary contains:
                    name: Monitor name if available.
                    width: Screen width in pixels.
                    height: Screen height in pixels.
                    x: Horizontal position in the virtual desktop.
                    y: Vertical position in the virtual desktop.
                    primary: True if this is the primary display.
            """
        data = []

        for m in get_monitors():
            data.append(
                {
                    "name": getattr(m, "name", "Unknown"),
                    "width": m.width,
                    "height": m.height,
                    "x": m.x,
                    "y": m.y,
                    "primary": (m.x == 0 and m.y == 0),
                }
            )

        return data

    def primary_monitor(self) -> Dict[str, Any]:
        """Get information about the primary monitor.

            Returns:
                Dictionary containing information about the primary display,
                including its name, resolution, position, and whether it is
                marked as the primary monitor.

            Raises:
                RuntimeError: If no primary monitor is found.
            """
        for monitor in self.monitors():
            if monitor["primary"]:
                return monitor

        raise RuntimeError("Primary monitor not found.")

    # ==========================================================
    # Brightness
    # ==========================================================

    def brightness(self, level: int | None = None) -> Any:
        """Get or set the display brightness.

            Args:
                level: Brightness percentage between 0 and 100.
                    If omitted, the current brightness is returned.
                    If provided, the display brightness is updated.

            Returns:
                Current brightness level when no value is supplied,
                otherwise a status message confirming the change.

            Raises:
                ValueError: If the brightness is outside the range 0-100.
            """
        if level is None:
            return sbc.get_brightness()

        if not 0 <= level <= 100:
            raise ValueError("Brightness must be between 0 and 100.")

        sbc.set_brightness(level)

        return f"Brightness set to {level}%."

    # ==========================================================
    # Rotation
    # ==========================================================

    def rotate(self, angle: int) -> str:
        """Rotate the primary display.

            Supported angles:
                0   : Landscape
                90  : Portrait
                180 : Landscape (Upside Down)
                270 : Portrait (Flipped)

            Args:
                angle: Rotation angle in degrees.

            Returns:
                Status message confirming the display rotation.

            Raises:
                ValueError: If the angle is not one of 0, 90, 180, or 270.
                RuntimeError: If Windows fails to rotate the display.
            """

        mapping = {
            0: win32con.DMDO_DEFAULT,
            90: win32con.DMDO_90,
            180: win32con.DMDO_180,
            270: win32con.DMDO_270,
        }

        if angle not in mapping:
            raise ValueError("Angle must be 0, 90, 180 or 270.")
        




        devmode = win32api.EnumDisplaySettings(
            None,
            win32con.ENUM_CURRENT_SETTINGS,
        )
        current = devmode.DisplayOrientation
        new = mapping[angle]

        # Swap only when moving between landscape and portrait
        if (current + new) % 2 == 1:
            devmode.PelsWidth, devmode.PelsHeight = (
                devmode.PelsHeight,
                devmode.PelsWidth,
            )

        devmode.DisplayOrientation = new
        devmode.Fields |= win32con.DM_DISPLAYORIENTATION

        result = win32api.ChangeDisplaySettings(devmode, 0) # type: ignore

        errors = {
                win32con.DISP_CHANGE_BADMODE: "Graphics mode not supported",
                win32con.DISP_CHANGE_BADFLAGS: "Invalid flags",
                win32con.DISP_CHANGE_BADPARAM: "Invalid parameters",
                win32con.DISP_CHANGE_FAILED: "Display driver rejected the request",
                win32con.DISP_CHANGE_RESTART: "Restart required",
                win32con.DISP_CHANGE_NOTUPDATED: "Registry update failed",
            }

        if result != win32con.DISP_CHANGE_SUCCESSFUL:
                raise RuntimeError(errors.get(result, f"Unknown error ({result})"))
        
        
        return f"Display rotated to {angle}°."

    # ==========================================================
    # Scaling
    # ==========================================================

    def scale(self) -> str:
        """Return display scaling information."""

        return (
            "Windows display scaling cannot be changed reliably "
            "through the Win32 API. It must be changed through "
            "the Windows Display Settings or newer Windows APIs."
        )