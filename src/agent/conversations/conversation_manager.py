"""
# ^ Responsibilities

    Receive user input
    Publish USER_MESSAGE
    Listen for ASK_USER
    Listen for AGENT_MESSAGE
    Listen for GOAL_COMPLETED
    Listen for GOAL_FAILED
    Update ConversationState

# ^ Conversation Manager will subscribe to

    ASK_USER

    CONFIRMATION_REQUIRED

    AGENT_MESSAGE

    GOAL_COMPLETED

    GOAL_FAILED

    ASK_HUMAN

# ^ Publish

    USER_MESSAGE

    USER_RESPONSE

    USER_CONFIRMED

    USER_CANCELLED

"""

from src.agent.events.event_bus import EventBus
from src.agent.events.event_handler import EventHandler
from src.agent.state.agent_state import AgentState
from src.agent.events.event_types import EventTypes
from src.agent.messages.messages import Message, MessageRole
from src.agent.events.event import Event


class ConversationManager(EventHandler):

    def __init__(
        self,
        state: AgentState,
        event_bus: EventBus,
    ) -> None:
        super().__init__()

        self._state = state
        self._event_bus = event_bus

        # self._register_events()

    # ^ ==========================================================
    # ^ Registration
    # ^ ==========================================================

    def _register_events(self) -> None:

        self._event_bus.subscribe(
            EventTypes.ASK_USER,
            self.handle,
        )

        self._event_bus.subscribe(
            EventTypes.AGENT_MESSAGE,
            self.handle,
        )
        self._event_bus.subscribe(
            EventTypes.CONFIRMATION_REQUIRED,
            self.handle,
        )
        self._event_bus.subscribe(
            EventTypes.GOAL_COMPLETED,
            self.handle,
        )
        self._event_bus.subscribe(
            EventTypes.GOAL_FAILED,
            self.handle,
        )

        self._event_bus.subscribe(
            EventTypes.ASK_HUMAN,
            self.handle,
        )

    # ^ ==========================
    # ^ Public API
    # ^ ==========================

    def received_user_message(self, message: str) -> None:
        """
        Receive a new message from the user.
        """
        msg = Message(
            role=MessageRole.USER,
            content=message,
        )

        self._state.conversation.conversation_history.append(msg)

        self._state.conversation.user_response = message

        self._state.conversation.waiting_for_user = False

        self._event_bus.publish(
            Event(
                event_type=EventTypes.USER_MESSAGE,
                source="ConversationManager",
                payload=message,
            )
        )

    def send_message(self, message: str) -> None:
        """
        Send a message to the user.
        """

        msg = Message(role=MessageRole.ASSISTANT, content=message)

        self._state.conversation.conversation_history.append(msg)

        print(f"Agent:{message}")

    def ask_question(self, question: str) -> None:
        """
        Ask the user for additional information.
        """

        self._state.conversation.pending_question = question
        self._state.conversation.waiting_for_user = True

        self.send_message(question)

    def request_confirmation(self, message: str) -> None:
        """
        Ask the user for confirmation.
        """

        self._state.conversation.pending_confirmation = message
        self._state.conversation.waiting_for_user = True

        self.send_message(message)

    def notify(self, message: str) -> None:
        """
        Notify the user.
        """

        self.send_message(message)

    def speak(self, message: str) -> None:
        """
        Speak a message.

        V1:
            Uses console output.
        """

        print(f"[Speech] {message}")

    def pause_for_user(self) -> None:
        """
        Pause execution until the user responds.
        """
        self._state.conversation.waiting_for_user = True

    def resume(self) -> None:
        """
        Resume execution.
        """

        self._state.conversation.waiting_for_user = False

    # ^ ==========================
    # ^ Event Handling
    # ^ ==========================

    def on_ask_user(self, event: Event):

        self.ask_question(event.payload)

    def on_agent_message(self, event: Event) -> None:

        self.send_message(event.payload)

    def on_confirmation_required(self, event: Event) -> None:

        self.request_confirmation(event.payload)

    def on_goal_completed(self, event: Event) -> None:

        self.notify("Task Completed successfully.")

    def on_goal_failed(self, event: Event) -> None:

        self.notify("Task Failed")

    def on_ask_human(self, event: Event) -> None:

        self.ask_question(event.payload)
