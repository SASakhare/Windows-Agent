from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:

    success: bool
    tool: str
    action: str
    result: Any
    error: str | None
    metadata: Any
