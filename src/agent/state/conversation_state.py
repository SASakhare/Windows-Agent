from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:

    role: MessageRole

    content: str

    timestamp: datetime


@dataclass
class ConversationState:

    conversation_history: List[Message] = field(default_factory=list)

    pending_question: str = ""

    pending_confirmation: str = ""

    user_response: str = ""

    waiting_for_user: bool = False
