from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.reasoner_state import ReasonerState


class ReasonerFormatter(BaseFormatter):
    """
    Converts ReasonerState into an LLM-friendly strategic reasoning summary.
    """

    def format(  # type: ignore
        self,
        state: ReasonerState,
    ) -> str:

        lines: list[str] = []

        lines.append("=" * 70)
        lines.append("REASONER STATE")
        lines.append("=" * 70)
        lines.append("")
        lines.append(
            "This section represents the agent's current understanding "
            "of the user's objective and long-term strategy."
        )
        lines.append(
            "Use it to maintain continuity between reasoning cycles."
        )
        lines.append("")

        # --------------------------------------------------
        # Objective
        # --------------------------------------------------

        lines.append("Current Objective")
        lines.append("-" * 30)

        lines.append(
            state.objective
            if state.objective
            else "No objective identified yet."
        )

        lines.append("")

        # --------------------------------------------------
        # Understanding
        # --------------------------------------------------

        lines.append("Current Understanding")
        lines.append("-" * 30)

        lines.append(
            state.understanding
            if state.understanding
            else "No understanding available."
        )

        lines.append("")

        # --------------------------------------------------
        # Strategy
        # --------------------------------------------------

        lines.append("Current Strategy")
        lines.append("-" * 30)

        lines.append(
            state.strategy
            if state.strategy
            else "No strategy defined."
        )

        lines.append("")

        # --------------------------------------------------
        # Current Focus
        # --------------------------------------------------

        lines.append("Current Focus")
        lines.append("-" * 30)

        lines.append(
            state.current_focus
            if state.current_focus
            else "No current focus."
        )

        lines.append("")

        # --------------------------------------------------
        # Planner Guidance
        # --------------------------------------------------

        lines.append("Planner Guidance")
        lines.append("-" * 30)

        lines.append(
            state.planner_guidance
            if state.planner_guidance
            else "No guidance available."
        )

        lines.append("")

        # --------------------------------------------------
        # Assumptions
        # --------------------------------------------------

        lines.append("Assumptions")
        lines.append("-" * 30)

        if state.assumptions:
            for assumption in state.assumptions:
                lines.append(f"• {assumption}")
        else:
            lines.append("No assumptions.")

        lines.append("")

        # --------------------------------------------------
        # Constraints
        # --------------------------------------------------

        lines.append("Constraints")
        lines.append("-" * 30)

        if state.constraints:
            for constraint in state.constraints:
                lines.append(f"• {constraint}")
        else:
            lines.append("No constraints.")

        lines.append("")

        # --------------------------------------------------
        # Lessons Learned
        # --------------------------------------------------

        lines.append("Lessons Learned")
        lines.append("-" * 30)

        if state.lessons:
            for lesson in state.lessons:
                lines.append(f"• {lesson}")
        else:
            lines.append("No lessons learned.")

        lines.append("")

        # --------------------------------------------------
        # Known Failures
        # --------------------------------------------------

        lines.append("Known Failures")
        lines.append("-" * 30)

        if state.known_failures:
            for failure in state.known_failures:
                lines.append(f"• {failure}")
        else:
            lines.append("No known failures.")

        lines.append("")

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        lines.append("Confidence")
        lines.append("-" * 30)

        lines.append(f"{state.confidence:.2f}")

        lines.append("")

        return "\n".join(lines)