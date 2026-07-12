from __future__ import annotations

from abc import ABC, abstractmethod

from src.agent.events.event import Event


class EventHandler(ABC):
    """
    Base class for all event subscribers.
    """

    def handle(self, event: Event) -> None:
        """
        Automatically dispatch an event to the matching handler.

        Example

        USER_MESSAGE

        ↓

        on_user_message()
        """

        method_name = f"on_{event.event_type.value}"

        handler = getattr(
            self,
            method_name,
            None,
        )

        if handler is None:
            self.on_unknown_event(event) # type: ignore
            return
        
        handler(event)


    def on_unknown_event(self, event: Event) -> None:
        """
            Called when no handler exists for an event.
        """
        
        pass