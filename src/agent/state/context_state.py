
from dataclasses import dataclass


@dataclass
class ContextState:

    planner_context: str = ""

    reflection_context: str = ""

    recovery_context: str = ""

    conversation_context: str = ""