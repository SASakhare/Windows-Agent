from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.reflection_state import ReflectionState


class ReflectionFormatter(BaseFormatter):
    """
    Formats the ReflectionState into a readable prompt section.
    """

    def format( # type: ignore
        self,
        reflection: ReflectionState,
    ) -> str:

        sections: list[str] = []

        sections.append(
            "==================== Reflection State ===================="
        )

        sections.append(
            "The Reflection node summarizes the outcome of the previous "
            "execution and determines whether the agent made progress, "
            "completed the goal, needs replanning, or is stuck."
        )

        sections.append("")

        sections.append("Progress Made")
        sections.append(f"- {reflection.progress_made}")
        sections.append("")

        sections.append("Goal Completed")
        sections.append(f"- {reflection.goal_completed}")
        sections.append("")

        sections.append("Needs Replanning")
        sections.append(f"- {reflection.needs_replanning}")
        sections.append("")

        sections.append("Failure Detected")
        sections.append(f"- {reflection.failure_detected}")
        sections.append("")

        sections.append("Agent Stuck")
        sections.append(f"- {reflection.agent_stuck}")
        sections.append("")

        sections.append("Confidence")
        sections.append(f"- {reflection.confidence:.2f}")
        sections.append("")

        sections.append("Verified")
        sections.append(f"- {reflection.verified}")
        sections.append("")

        sections.append("Reason")
        sections.append(
            f"- {reflection.reason or 'No reason available.'}"
        )
        sections.append("")

        sections.append("Summary")
        sections.append(
            f"- {reflection.summary or 'No summary available.'}"
        )

        return "\n".join(sections)