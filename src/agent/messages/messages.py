from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import DefaultDict


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:

    role: MessageRole

    content: str

    timestamp: datetime = field(default_factory=datetime.utcnow)
