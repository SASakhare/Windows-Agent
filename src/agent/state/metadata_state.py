from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MetadataState:

    task_id: str = ""

    started_at: datetime | None = None

    updated_at: datetime | None = None

    agent_status: AgentStatus = AgentStatus.IDLE