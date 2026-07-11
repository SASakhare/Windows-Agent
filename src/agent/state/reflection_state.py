'''
Reflection answers:

    Was the action successful?
    How confident am I?
    Why did I reach this conclusion?
'''

from dataclasses import dataclass
from enum import Enum


class ReflectionResult(Enum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class ReflectionState:

    reflection_result: ReflectionResult = ReflectionResult.UNKNOWN

    confidence: float = 0.0

    verified: bool = False

    reason: str = ""