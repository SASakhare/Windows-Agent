from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Action:
    """
    Represent a single executable action generated y the Planner.

    """

    tool: str  # * Tool to call

    action: str  # * which action has sto perform on that tool

    arguments: dict[str, Any] = field(default_factory=dict)

    expected_outcome: str = ""
