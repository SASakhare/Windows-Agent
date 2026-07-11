from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime


class GoalStatus(Enum):

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class GoalState:

    goal_id: str = ""

    user_goal: str = ""

    status: GoalStatus = GoalStatus.IDLE

    current_subgoal: str = ""

    subtasks: List[str] = field(default_factory=list)

    completed_tasks: List[str] = field(default_factory=list)

    active_task_index: int = 0

    created_at:datetime|None=None


