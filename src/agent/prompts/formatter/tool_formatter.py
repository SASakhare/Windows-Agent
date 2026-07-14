from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.tools.registry import ToolRegistry


class ToolFormatter(BaseFormatter):
    """
    Converts ToolRegistry into LLM-friendly documentation.
    """

    def format(  # type: ignore
        self,
        tool_registry: ToolRegistry,
    ) -> str:

        sections: list[str] = []

        schemas = tool_registry.get_all_schemas()

        for tool_name, schema in schemas.items():

            sections.append("=" * 70)
            sections.append(f"Tool : {tool_name}")
            sections.append("=" * 70)

            description = (
                schema.get("description", "").strip()
                or "No description available."
            )

            sections.append("")
            sections.append("Purpose")
            sections.append("-------")
            sections.append(description)
            sections.append("")

            sections.append("Available Actions")
            sections.append("-----------------")

            for action in schema["actions"]:

                action_name = action["name"]

                params = action["parameters"]

                signature = ", ".join(params.keys())

                sections.append(f"• {action_name}({signature})")

                action_description = (
                    action.get("description", "").strip()
                )

                if action_description:
                    sections.append(
                        f"    Description : {action_description}"
                    )

                if params:

                    sections.append(
                        "    Required Arguments:"
                    )

                    for name, info in params.items():

                        required = (
                            "Required"
                            if info["required"]
                            else "Optional"
                        )

                        default = ""

                        if (
                            not info["required"]
                            and info["default"] is not None
                        ):
                            default = (
                                f" (default={info['default']})"
                            )

                        sections.append(
                            f"      • {name}"
                            f" : {info['type']}"
                            f" [{required}]"
                            f"{default}"
                        )

                else:

                    sections.append(
                        "    Required Arguments : None"
                    )

                sections.append("")

            sections.append("")

        return "\n".join(sections)