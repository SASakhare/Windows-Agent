from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.word_state import WorldState


class WorldFormatter(BaseFormatter):
    """
    Converts WorldState into an LLM-friendly environment summary.
    """

    def format(  # type: ignore
        self,
        world: WorldState,
    ) -> str:

        lines: list[str] = []

        lines.append("=" * 70)
        lines.append("WORLD STATE")
        lines.append("=" * 70)
        lines.append("")
        lines.append(
            "The World State represents the agent's current understanding "
            "of the environment."
        )
        lines.append(
            "Use this information to avoid repeating actions and to decide "
            "the next best action."
        )
        lines.append("")

        if not world.data:
            lines.append("No world information is currently available.")
            lines.append(
                "Assume nothing about the environment and rely on available "
                "tools if inspection is required."
            )
            return "\n".join(lines)

        for category, value in world.data.items():

            lines.append(f"{category}")
            lines.append("-" * len(str(category)))

            if isinstance(value, dict):

                if not value:
                    lines.append("No information available.")
                else:
                    for key, val in value.items():
                        lines.append(f"• {key}: {val}")

            elif isinstance(value, list):

                if not value:
                    lines.append("None")
                else:
                    for item in value:
                        lines.append(f"• {item}")

            else:

                lines.append(str(value))

            lines.append("")

        return "\n".join(lines)