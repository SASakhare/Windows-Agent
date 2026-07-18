from dataclasses import dataclass
from enum import Enum


class RecoveryStrategy(Enum):
    NONE = "none"
    CONTINUE = "continue"
    RETRY = "retry"
    REPLAN = "replan"
    FALLBACK_TOOL = "fallback_tool"
    ASK_USER = "ask_user"
    ABORT = "abort"


@dataclass
class RecoveryState:

    strategy: RecoveryStrategy = RecoveryStrategy.NONE

    fallback_tool: str = ""

    recovery_attempts: int = 0

    confidence: float = 0.0

    verified: bool = False

    reason: str = ""

    summary: str = ""

    last_failure: str = ""