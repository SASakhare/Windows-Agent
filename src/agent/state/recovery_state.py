from dataclasses import dataclass
from enum import Enum


class RecoveryStrategy(Enum):
    NONE = "none"
    RETRY = "retry"
    FALLBACK_TOOL = "fallback_tool"
    REPLAN = "replan"
    ASK_USER = "ask_user"
    ABORT = "abort"


@dataclass
class RecoveryState:

    recovery_strategy: RecoveryStrategy = RecoveryStrategy.NONE

    fallback_tool: str = ""

    recovery_attempts: int = 0

    reason: str = ""

    last_failure: str = ""