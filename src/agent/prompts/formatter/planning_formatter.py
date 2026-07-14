from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.planning_state import PlanningState


class PlanningFormatter(BaseFormatter):
    """
    Converts PlanningState into an LLM-friendly planning summary.
    """

    def format(  # type: ignore
        self,
        state: PlanningState,
    ) -> str:

        lines: list[str] = []

        lines.append("=" * 70)
        lines.append("PLANNING STATE")
        lines.append("=" * 70)
        lines.append("")
        lines.append(
            "This section describes the current progress of execution."
        )
        lines.append(
            "Use it to avoid repeating completed actions and to determine"
        )
        lines.append(
            "the next best action."
        )
        lines.append("")

        # --------------------------------------------------
        # Current Action
        # --------------------------------------------------

        lines.append("Current Action")
        lines.append("-" * 30)

        if state.current_action:
            action = state.current_action

            lines.append(f"Tool      : {action.tool}")
            lines.append(f"Action    : {action.action}")

            if action.arguments:
                lines.append("Arguments :")

                for key, value in action.arguments.items():
                    lines.append(f"  • {key} = {value}")
            else:
                lines.append("Arguments : None")
        else:
            lines.append("No action has been planned yet.")

        lines.append("")

        # --------------------------------------------------
        # Expected Outcome
        # --------------------------------------------------

        lines.append("Expected Outcome")
        lines.append("-" * 30)

        if state.expected_outcome:
            lines.append(state.expected_outcome)
        else:
            lines.append("No expected outcome available.")

        lines.append("")

        # --------------------------------------------------
        # Planning History
        # --------------------------------------------------

        lines.append("Planning History")
        lines.append("-" * 30)

        if state.plan:

            for index, step in enumerate(state.plan, start=1):
                lines.append(f"{index}. {step}")

        else:
            lines.append("No previous planning history.")

        lines.append("")

        # --------------------------------------------------
        # Goal Status
        # --------------------------------------------------

        lines.append("Goal Status")
        lines.append("-" * 30)

        if state.goal_completed:
            lines.append("The planner believes the goal is completed.")
        else:
            lines.append("The goal has not been completed yet.")

        lines.append("")

        return "\n".join(lines)