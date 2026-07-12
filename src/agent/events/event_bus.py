"""
The EventBus should do one thing only:

    Deliver events from publishers to subscribers.

This is the heart of EDA.

Responsibilities:

    Register subscribers
    Remove subscribers
    Publish events
    Notify listeners


Public API

    subscribe()

    unsubscribe()

    publish()

    clear()

    listener_count()

"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict


from src.agent.events.event import Event
from src.agent.events.event_types import EventTypes

EventCallback = Callable[[Event], None]


class EventBus:
    """
    In-memory publish/subscribe event bus.

    Components communicate by publishing events.
    Other components subscribe to event types they care about
    """

    def __init__(self) -> None:

        # * here we mapping number of subscriber/callback/services to single eventType
        self._subscribers: DefaultDict[
            EventTypes,
            list[EventCallback],
        ] = defaultdict(list)

    # ^ ==========================================================
    # ^ Subscription
    # ^ ==========================================================

    def subscribe(
        self,
        event_type: EventTypes,
        callback: EventCallback,
    ) -> None:
        """
        Register a callback for an event type.
        """

        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)

    def unsubscribe(
        self,
        event_type: EventTypes,
        callback: EventCallback,
    ) -> None:
        """
        Remove a callback from an event type.
        """

        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    # ^ ==========================================================
    # ^ Publishing
    # ^ ==========================================================

    def publish(
        self,
        event: Event,
    ) -> None:
        """
        Publish an event to all subscribers.
        """

        callbacks = self._subscribers.get(event.event_type, [])

        for callback in callbacks:
            callback(event)  # * later we run each callback parallel

    # ^ ==========================================================
    # ^ Utility
    # ^ ==========================================================

    def clear(self) -> None:
        """
        Remove all subscribers.
        """

        self._subscribers.clear()

    def listener_count(
        self,
        event_type: EventTypes | None = None,
    ) -> int:
        """
        Return number of registered listeners.

        If event_type is None,
        returns total listeners across all events.
        """

        if event_type is not None:

            return len(self._subscribers[event_type])

        return sum(len(callbacks) for callbacks in self._subscribers.values())

    def has_subscribers(
        self,
        event_type: EventTypes,
    ) -> bool:
        """
        Check whether an event type has listeners.
        """

        return len(self._subscribers[event_type]) > 0

        # publish_async()

        # subscribe_once()

        # event_history()

        # middleware()

        # priority listeners()

        # event replay()

        # thread-safe publishing()

        # async callbacks()
