from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.recovery_state import (
    RecoveryState,
    RecoveryStrategy,
)


class RecoveryFormatter(BaseFormatter):
    """
    Converts RecoveryState into an LLM-friendly recovery summary.
    """

    def format(  # type: ignore
        self,
        state: RecoveryState,
    ) -> str:

        lines: list[str] = []

        lines.append("=" * 70)
        lines.append("RECOVERY STATE")
        lines.append("=" * 70)
        lines.append("")
        lines.append(
            "This section describes the current recovery status of the agent."
        )
        lines.append(
            "Use it to understand previous recovery attempts and determine"
        )
        lines.append(
            "whether another recovery action is required."
        )
        lines.append("")

        # --------------------------------------------------
        # Recovery Strategy
        # --------------------------------------------------

        lines.append("Recovery Strategy")
        lines.append("-" * 30)

        if state.strategy != RecoveryStrategy.NONE:
            lines.append(f"Strategy : {state.strategy.value}")
        else:
            lines.append("No recovery strategy has been selected.")

        lines.append("")

        # --------------------------------------------------
        # Recovery Attempts
        # --------------------------------------------------

        lines.append("Recovery Attempts")
        lines.append("-" * 30)

        lines.append(
            f"Attempts : {state.recovery_attempts}"
        )

        lines.append("")

        # --------------------------------------------------
        # Fallback Tool
        # --------------------------------------------------

        lines.append("Fallback Tool")
        lines.append("-" * 30)

        if state.fallback_tool:
            lines.append(state.fallback_tool)
        else:
            lines.append("No fallback tool selected.")

        lines.append("")

        # --------------------------------------------------
        # Last Failure
        # --------------------------------------------------

        lines.append("Last Failure")
        lines.append("-" * 30)

        if state.last_failure:
            lines.append(state.last_failure)
        else:
            lines.append("No previous failure recorded.")

        lines.append("")

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        lines.append("Confidence")
        lines.append("-" * 30)

        lines.append(f"{state.confidence:.2f}")

        lines.append("")

        # --------------------------------------------------
        # Verification
        # --------------------------------------------------

        lines.append("Verification")
        lines.append("-" * 30)

        if state.verified:
            lines.append("The recovery decision has been verified.")
        else:
            lines.append("The recovery decision has not been verified.")

        lines.append("")

        # --------------------------------------------------
        # Reason
        # --------------------------------------------------

        lines.append("Reason")
        lines.append("-" * 30)

        if state.reason:
            lines.append(state.reason)
        else:
            lines.append("No recovery reason available.")

        lines.append("")

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        lines.append("Summary")
        lines.append("-" * 30)

        if state.summary:
            lines.append(state.summary)
        else:
            lines.append("No recovery summary available.")

        lines.append("")

        return "\n".join(lines)