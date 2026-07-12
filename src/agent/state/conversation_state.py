from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List
from src.agent.messages.messages import Message,MessageRole



@dataclass
class ConversationState:

    conversation_history: List[Message] = field(default_factory=list)

    pending_question: str = ""

    pending_confirmation: str = ""

    user_response: str = ""

    waiting_for_user: bool = False
