# * Network Tool for Agent

import socket
import subprocess
from typing import Any, Dict, List, Optional

import psutil

from src.agent.utils.admin import Admin
from src.agent.tools.base_tool import BaseTool


class NetworkTool(BaseTool):
    """Tool for managing and inspecting Windows network state.

    Provides methods to control Wi-Fi, inspect local and public IP
    addresses, test connectivity, resolve DNS, and enumerate network
    adapters.
    """

    def __init__(self) -> None:
        """Initialize the network tool."""
        pass

    @property
    def name(self) -> str:
        return "network"

    @property
    def description(self) -> str:
        return "Manage and inspect Windows network operations."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "wifi_on": self.wifi_on,
            "wifi_off": self.wifi_off,
            "ip": self.ip,
            "public_ip": self.public_ip,
            "ping": self.ping,
            "dns_lookup": self.dns_lookup,
            "internet_available": self.internet_available,
            "adapters": self.adapters,
            "connect_wifi": self.connect_wifi,
            "disconnect_wifi": self.disconnect_wifi,
            "available_wifi": self.available_wifi,
            "saved_wifi_profiles": self.saved_wifi_profiles,
        }

        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ==========================================================
    # Wi-Fi Radio Control
    # ==========================================================

    def wifi_on(self, interface: str = "Wi-Fi") -> str:
        """Enable the Wi-Fi network adapter.

        Args:
            interface: Name of the wireless network interface.

        Returns:
            Status message.

        Raises:
            PermissionError: If not running with administrator privileges.
            RuntimeError: If the command fails.
        """
        Admin.require_admin()

        result = subprocess.run(
            ["netsh", "interface", "set", "interface", interface, "enabled"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to enable Wi-Fi interface '{interface}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return f"Wi-Fi interface '{interface}' enabled."

    def wifi_off(self, interface: str = "Wi-Fi") -> str:
        """Disable the Wi-Fi network adapter.

        Args:
            interface: Name of the wireless network interface.

        Returns:
            Status message.

        Raises:
            PermissionError: If not running with administrator privileges.
            RuntimeError: If the command fails.
        """
        Admin.require_admin()

        result = subprocess.run(
            ["netsh", "interface", "set", "interface", interface, "disabled"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to disable Wi-Fi interface '{interface}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return f"Wi-Fi interface '{interface}' disabled."

    # ==========================================================
    # IP Information
    # ==========================================================

    def ip(self) -> Dict[str, str]:
        """Get the local machine's hostname and private IP address.

        Returns:
            Dictionary containing:
                hostname: The machine's network hostname.
                local_ip: The primary local IP address.
        """
        hostname = socket.gethostname()

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()
        except OSError:
            local_ip = socket.gethostbyname(hostname)

        return {
            "hostname": hostname,
            "local_ip": local_ip,
        }

    def public_ip(self, timeout: float = 5.0) -> str:
        """Get the machine's public-facing IP address.

        Args:
            timeout: Request timeout in seconds.

        Returns:
            The public IP address as a string.

        Raises:
            RuntimeError: If the public IP could not be determined.
        """
        import urllib.request

        try:
            with urllib.request.urlopen(
                "https://api.ipify.org", timeout=timeout
            ) as response:
                return response.read().decode("utf-8").strip()
        except Exception as exc:
            raise RuntimeError(f"Could not determine public IP: {exc}") from exc

    # ==========================================================
    # Connectivity
    # ==========================================================

    def ping(self, host: str = "8.8.8.8", count: int = 4) -> Dict[str, Any]:
        """Ping a host to test reachability and latency.

        Args:
            host: Hostname or IP address to ping.
            count: Number of echo requests to send.

        Returns:
            Dictionary containing:
                host: The target host.
                success: Whether the host responded.
                output: Raw command output.
        """
        result = subprocess.run(
            ["ping", "-n", str(count), host],
            capture_output=True,
            text=True,
            check=False,
        )

        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout,
        }

    def dns_lookup(self, hostname: str) -> str:
        """Resolve a hostname to an IP address.

        Args:
            hostname: The hostname to resolve.

        Returns:
            The resolved IP address.

        Raises:
            RuntimeError: If the hostname could not be resolved.
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror as exc:
            raise RuntimeError(f"DNS lookup failed for '{hostname}': {exc}") from exc

    def internet_available(self, timeout: float = 3.0) -> bool:
        """Check whether an internet connection is currently available.

        Args:
            timeout: Connection timeout in seconds.

        Returns:
            True if internet is reachable, False otherwise.
        """
        try:
            sock = socket.create_connection(("8.8.8.8", 53), timeout=timeout)
            sock.close()
            return True
        except OSError:
            return False

    def available_wifi(self) -> List[Dict[str, Any]]:
        """Scan for nearby Wi-Fi networks.

        Returns:
            List of dictionaries. Each dictionary contains:
                ssid: Network name.
                authentication: Authentication method.
                encryption: Encryption type.
                signal: Signal strength percentage.
                radio: Wi-Fi standard/radio type.
                channel: Operating channel.
                bssid: List of access point MAC addresses.

        Raises:
            RuntimeError: If the scan command fails.
        """
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to scan Wi-Fi networks: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        lines = result.stdout.splitlines()

        networks: List[Dict[str, Any]] = []
        network: Optional[Dict[str, Any]] = None

        for line in lines:
            line = line.strip()

            if line.startswith("SSID "):
                if network:
                    networks.append(network)

                network = {
                    "ssid": line.split(":", 1)[1].strip(),
                    "authentication": "",
                    "encryption": "",
                    "signal": "",
                    "radio": "",
                    "channel": "",
                    "bssid": [],
                }

            elif network is None:
                continue

            elif line.startswith("Authentication"):
                network["authentication"] = line.split(":", 1)[1].strip()

            elif line.startswith("Encryption"):
                network["encryption"] = line.split(":", 1)[1].strip()

            elif line.startswith("Signal"):
                network["signal"] = line.split(":", 1)[1].strip()

            elif line.startswith("Radio type"):
                network["radio"] = line.split(":", 1)[1].strip()

            elif line.startswith("Channel"):
                network["channel"] = line.split(":", 1)[1].strip()

            elif line.startswith("BSSID"):
                network["bssid"].append(line.split(":", 1)[1].strip())

        if network:
            networks.append(network)

        return networks

    # ==========================================================
    # Adapters
    # ==========================================================

    def adapters(self) -> Dict[str, List[Dict[str, Any]]]:
        """Enumerate network adapters and their addresses/status.

        Returns:
            Dictionary mapping adapter name to a list of address
            entries (family, address, netmask, is_up).
        """
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        result: Dict[str, List[Dict[str, Any]]] = {}

        for name, entries in addrs.items():
            is_up = stats[name].isup if name in stats else False
            result[name] = [
                {
                    "family": getattr(entry.family, "name", str(entry.family)),
                    "address": entry.address,
                    "netmask": entry.netmask,
                    "is_up": is_up,
                }
                for entry in entries
            ]

        return result

    # ==========================================================
    # Wi-Fi Network Connections
    # ==========================================================

    def connect_wifi(self, ssid: str, profile: Optional[str] = None) -> str:
        """Connect to a Wi-Fi network using a saved profile.

        Args:
            ssid: Name of the Wi-Fi network to connect to.
            profile: Profile name to use, if different from the SSID.

        Returns:
            Status message.

        Raises:
            RuntimeError: If the connect command fails.
        """
        profile_name = profile or ssid

        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={profile_name}", f"ssid={ssid}"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to connect to '{ssid}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return f"Connecting to Wi-Fi network '{ssid}'."

    def disconnect_wifi(self, interface: str = "Wi-Fi") -> str:
        """Disconnect from the current Wi-Fi network.

        Args:
            interface: Name of the wireless network interface.

        Returns:
            Status message.

        Raises:
            RuntimeError: If the disconnect command fails.
        """
        result = subprocess.run(
            ["netsh", "wlan", "disconnect", f"interface={interface}"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to disconnect Wi-Fi on '{interface}': "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        return "Wi-Fi disconnected."

    def saved_wifi_profiles(self) -> List[str]:
        """Return all saved Wi-Fi profiles.

        Returns:
            List of saved profile names.

        Raises:
            RuntimeError: If the command fails.
        """
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to list Wi-Fi profiles: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        profiles = []

        for line in result.stdout.splitlines():
            if "All User Profile" in line:
                profiles.append(line.split(":", 1)[1].strip())

        return profiles


if __name__ == "__main__":
    tool = NetworkTool()

    print("=== Local IP Info ===")
    print(tool.ip())

    print("\n=== Ping Test ===")
    print(tool.ping("8.8.8.8"))

    print("\n=== Internet Available ===")
    print(tool.internet_available())

    print("\n=== Adapters ===")
    print(tool.adapters())