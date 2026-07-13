"""
Responsibility :
    Represents a single event flowing through the system.


Every event should contain

    event_id

    event_type

    source

    timestamp

    payload


"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from src.agent.events.event_types import EventTypes


@dataclass(slots=True)
class Event:
    """
    Represent a single event flowing trough the EventBus.

    Event components communicates by publishing and subscribing to
    Event Objects.

    """

    event_type: EventTypes

    source: str

    payload: Any = None

    event_id: str = field(default_factory=lambda: str(uuid4()))

    timestamp: datetime = field(default_factory=datetime.utcnow)
