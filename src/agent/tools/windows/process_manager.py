# * Process Manager Tool for Agent

import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from base_tool import BaseTool
import psutil


class ProcessManager(BaseTool):
    """Tools for managing operating system processes.

    Every lookup/control method accepts either `pid` or `name` (never both).
    `pid` is preferred for reliability; `name` is a convenience for matching
    a process by its executable name (case-insensitive, exact match on
    `psutil.Process.name()`, e.g. "chrome.exe" or "Code.exe").
    """

    def __init__(self) -> None:
        """Initialize the process manager."""
        pass

    @property
    def name(self) -> str:
        return "process_manager"

    @property
    def description(self) -> str:
        return (
            "A tool for managing operating system processes. "
            "Supports listing, starting, stopping, and monitoring processes."
        )

    def execute(self, action: str, **kwargs) -> Any:

        actions = {
            # Process Information
            "list_processes": self.list_processes,
            "running_apps": self.running_apps,
            "get_process": self.get_process,
            "get_process_by_name": self.get_process_by_name,
            "is_running": self.is_running,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_usage": self.disk_usage,
            # Process Control
            "start_process": self.start_process,
            "stop_process": self.stop_process,
            "kill_process": self.kill_process,
            "restart_process": self.restart_process,
            # Waiting / Synchronization
            "wait_for_process": self.wait_for_process,
            "wait_until_exit": self.wait_until_exit,
            # Process Relationships
            "children": self.children,
            "process_tree": self.process_tree,
        }
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")

        return actions[action](**kwargs)

    # ^ ==========================================================
    # ^ Internal helpers
    # ^ ==========================================================

    @staticmethod
    def _resolve_args(name: Optional[str], pid: Optional[int]) -> None:
        """Validate that exactly one of name/pid was provided."""
        if name is None and pid is None:
            raise ValueError("Must provide either 'name' or 'pid'.")
        if name is not None and pid is not None:
            raise ValueError("Provide only one of 'name' or 'pid', not both.")

    @staticmethod
    def _find_by_name(name: str) -> List[psutil.Process]:
        """Return all live processes whose name matches (case-insensitive)."""
        matches = []
        target = name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == target:
                    matches.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return matches

    def _resolve_process(
        self, name: Optional[str] = None, pid: Optional[int] = None
    ) -> psutil.Process:
        """Resolve a single psutil.Process from either a pid or a name.

        If multiple processes share `name`, the one with the highest CPU
        usage snapshot is returned as the most likely "active" instance.
        """
        self._resolve_args(name, pid)

        if pid is not None:
            if not psutil.pid_exists(pid):
                raise ProcessLookupError(f"No process with PID {pid}.")
            return psutil.Process(pid)

        matches = self._find_by_name(name)  # type: ignore
        if not matches:
            raise ProcessLookupError(f"No running process named '{name}'.")
        if len(matches) == 1:
            return matches[0]
        # Multiple matches: pick busiest as best guess.
        return max(matches, key=lambda p: self._safe_cpu(p))

    @staticmethod
    def _safe_cpu(proc: psutil.Process) -> float:
        try:
            return proc.cpu_percent(interval=0.0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return 0.0

    @staticmethod
    def _proc_to_dict(proc: psutil.Process) -> Dict[str, Any]:
        """Serialize a psutil.Process into a plain dict."""
        try:
            with proc.oneshot():
                return {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "status": proc.status(),
                    "cpu_percent": proc.cpu_percent(interval=0.0),
                    "memory_mb": round(proc.memory_info().rss / (1024 * 1024), 2),
                    "create_time": proc.create_time(),
                    "cmdline": proc.cmdline(),
                    "username": proc.username(),
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return {"pid": proc.pid, "name": None, "status": "unavailable"}

    # ^ ==========================================================
    # ^ 1) Process Information
    # ^ ==========================================================

    def list_processes(self) -> List[Dict[str, Any]]:
        """Return information about all running processes."""
        return [self._proc_to_dict(p) for p in psutil.process_iter()]

    def running_apps(self) -> List[Dict[str, Any]]:
        """Return only processes that have a visible application window.

        On platforms without window-enumeration support, falls back to
        heuristically filtering out kernel/system processes.
        """
        apps: List[Dict[str, Any]] = []
        try:
            import pygetwindow as gw  # optional, only used if available

            titled_pids = set()
            for window in gw.getAllWindows():
                if window.title:
                    titled_pids.add(window._hWnd)  # platform-specific
            for proc in psutil.process_iter():
                if proc.pid in titled_pids:
                    apps.append(self._proc_to_dict(proc))
            return apps
        except ImportError:
            pass

        # Fallback heuristic: processes with a non-empty cmdline and a name
        # that isn't a typical background/system process.
        for proc in psutil.process_iter(["name", "cmdline"]):
            try:
                if proc.info["cmdline"] and proc.ppid() != 0:
                    apps.append(self._proc_to_dict(proc))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return apps

    def get_process(self, pid: int) -> Dict[str, Any]:
        """Return detailed info for a single process by PID."""
        if not psutil.pid_exists(pid):
            raise ProcessLookupError(f"No process with PID {pid}.")
        return self._proc_to_dict(psutil.Process(pid))

    def get_process_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Return detailed info for all processes matching `name`."""
        matches = self._find_by_name(name)
        if not matches:
            raise ProcessLookupError(f"No running process named '{name}'.")
        return [self._proc_to_dict(p) for p in matches]

    def is_running(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> bool:
        """Check whether a process is currently running."""
        self._resolve_args(name, pid)
        if pid is not None:
            return psutil.pid_exists(pid)
        return len(self._find_by_name(name)) > 0 # type: ignore

    def cpu_usage(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> float:
        """Return CPU usage percentage for a process."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            # Short sample window for a meaningful reading.
            return proc.cpu_percent(interval=0.1)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc

    def memory_usage(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Return memory usage statistics."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            mem = proc.memory_info()
            return {
                "rss_mb": round(mem.rss / (1024 * 1024), 2),
                "vms_mb": round(mem.vms / (1024 * 1024), 2),
                "percent": round(proc.memory_percent(), 2),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc

    def disk_usage(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Return disk I/O statistics for a process."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            io = proc.io_counters()
            return {
                "read_mb": round(io.read_bytes / (1024 * 1024), 2),
                "write_mb": round(io.write_bytes / (1024 * 1024), 2),
                "read_count": io.read_count,
                "write_count": io.write_count,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc
        except AttributeError as exc:
            raise NotImplementedError(
                "io_counters() is not supported on this platform."
            ) from exc

    # ==========================================================
    # 2) Process Control
    # ==========================================================

    def start_process(
        self,
        executable: str,
        arguments: Optional[List[str]] = None,
        cwd: Optional[str] = None,
    ) -> str:
        """Start a new process and return its PID as a string."""
        if not executable:
            raise ValueError("'executable' must be a non-empty string.")

        cmd = [executable] + (arguments or [])
        work_dir = str(Path(cwd)) if cwd else None

        try:
            process = subprocess.Popen(cmd, cwd=work_dir)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Executable not found: '{executable}'") from exc

        return f"Started '{executable}' with PID {process.pid}"

    def stop_process(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> str:
        """Gracefully terminate a process (SIGTERM equivalent)."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            proc.terminate()
            proc.wait(timeout=5)
            return f"Process {proc.pid} ('{proc.name()}') terminated gracefully."
        except psutil.TimeoutExpired:
            return f"Process {proc.pid} did not exit within timeout; still running."
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc

    def kill_process(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> str:
        """Force kill a process (SIGKILL equivalent)."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            proc.kill()
            proc.wait(timeout=5)
            return f"Process {proc.pid} ('{proc.name()}') killed."
        except psutil.TimeoutExpired:
            return f"Kill signal sent to {proc.pid}, but exit not confirmed."
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc

    def restart_process(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
    ) -> str:
        """Restart a running process (stop, then relaunch its original command)."""
        proc = self._resolve_process(name=name, pid=pid)
        try:
            cmdline = proc.cmdline()
            cwd = proc.cwd()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc

        if not cmdline:
            raise RuntimeError(
                f"Cannot restart process {proc.pid}: original command line unavailable."
            )

        self.stop_process(pid=proc.pid)
        new_proc = subprocess.Popen(cmdline, cwd=cwd)
        return f"Restarted '{cmdline[0]}' as new PID {new_proc.pid}"

    # ==========================================================
    # 3) Waiting / Synchronization
    # ==========================================================

    def wait_for_process(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Block until a process with the given name/pid appears (starts).

        Returns info about the process once found. Raises TimeoutError if
        `timeout` (seconds) elapses first.
        """
        self._resolve_args(name, pid)
        start = time.monotonic()

        while True:
            if pid is not None:
                if psutil.pid_exists(pid):
                    return self._proc_to_dict(psutil.Process(pid))
            else:
                matches = self._find_by_name(name) # type: ignore
                if matches:
                    return self._proc_to_dict(matches[0])

            if timeout is not None and (time.monotonic() - start) >= timeout:
                target = f"PID {pid}" if pid is not None else f"name '{name}'"
                raise TimeoutError(f"Timed out waiting for process {target} to start.")
            time.sleep(0.25)

    def wait_until_exit(
        self,
        name: Optional[str] = None,
        pid: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> str:
        """Block until a running process exits.

        If the process isn't running at all, returns immediately. Raises
        TimeoutError if `timeout` (seconds) elapses before exit.
        """
        self._resolve_args(name, pid)

        if pid is not None:
            if not psutil.pid_exists(pid):
                return f"Process {pid} is not running."
            proc = psutil.Process(pid)
            try:
                proc.wait(timeout=timeout)
                return f"Process {pid} has exited."
            except psutil.TimeoutExpired as exc:
                raise TimeoutError(f"Timed out waiting for PID {pid} to exit.") from exc

        # By name: wait until *all* matching processes exit.
        start = time.monotonic()
        while True:
            matches = self._find_by_name(name) # type: ignore
            if not matches:
                return f"All processes named '{name}' have exited."
            if timeout is not None and (time.monotonic() - start) >= timeout:
                raise TimeoutError(f"Timed out waiting for '{name}' to exit.")
            time.sleep(0.25)

    # ==========================================================
    # 4) Process Relationships
    # ==========================================================

    def children(self, pid: int, recursive: bool = False) -> List[Dict[str, Any]]:
        """Return direct (or all recursive) child processes of `pid`."""
        if not psutil.pid_exists(pid):
            raise ProcessLookupError(f"No process with PID {pid}.")
        proc = psutil.Process(pid)
        try:
            kids = proc.children(recursive=recursive)
        except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
            raise ProcessLookupError(str(exc)) from exc
        return [self._proc_to_dict(c) for c in kids]

    def process_tree(self, pid: int) -> Dict[str, Any]:
        """Return a nested dict representing the process and its descendants."""
        if not psutil.pid_exists(pid):
            raise ProcessLookupError(f"No process with PID {pid}.")

        def build(proc: psutil.Process) -> Dict[str, Any]:
            node = self._proc_to_dict(proc)
            try:
                node["children"] = [build(c) for c in proc.children(recursive=False)]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                node["children"] = []
            return node

        return build(psutil.Process(pid))
