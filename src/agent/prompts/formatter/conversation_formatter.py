from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.conversation_state import ConversationState


class ConversationFormatter(BaseFormatter):
    """
    Converts ConversationState into an LLM-friendly conversation summary.
    """

    def format(  # type: ignore
        self,
        state: ConversationState,
    ) -> str:

        if not state.conversation_history:
            return (
                "No previous conversation.\n"
                "This is the first interaction with the user."
            )

        lines: list[str] = []

        lines.append("=" * 70)
        lines.append("CONVERSATION HISTORY")
        lines.append("=" * 70)
        lines.append("")
        lines.append(
            "Use this conversation to understand the user's intent, "
            "previous clarifications, and any constraints."
        )
        lines.append("")

        for i, message in enumerate(state.conversation_history, start=1):

            role = message.role.value.capitalize()

            lines.append(f"{i}. {role}")
            lines.append(f"   {message.content}")
            lines.append("")

        last_message = state.conversation_history[-1]

        lines.append("-" * 70)
        lines.append("LATEST USER INPUT")
        lines.append("-" * 70)
        lines.append("")

        lines.append(
            f"{last_message.role.value.capitalize()}: "
            f"{last_message.content}"
        )
        lines.append("")

        return "\n".join(lines)