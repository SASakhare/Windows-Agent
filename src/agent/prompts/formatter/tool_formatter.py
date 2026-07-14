from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.tools.registry import ToolRegistry


class ToolFormatter(BaseFormatter):
    """
    Converts ToolRegistry into compact planner documentation.
    """

    def format(  # type: ignore
        self,
        tool_registry: ToolRegistry,
    ) -> str:

        sections: list[str] = []

        schemas = tool_registry.get_all_schemas()

        for tool_name, schema in schemas.items():

            sections.append("=" * 60)
            sections.append(f"TOOL: {tool_name}")
            sections.append("=" * 60)

            description = (
                schema.get("description", "").strip().split("\n")[0]
            )

            sections.append("")
            sections.append(f"Purpose: {description}")
            sections.append("")
            sections.append("Available Actions")
            sections.append("-----------------")

            for action in schema["actions"]:

                params = ", ".join(action["parameters"].keys())

                signature = (
                    f"{action['name']}({params})"
                    if params
                    else f"{action['name']}()"
                )

                sections.append(f"• {signature}")

                desc = (
                    action.get("description", "")
                    .strip()
                    .split("\n")[0]
                )

                if desc:
                    sections.append(f"  {desc}")

                sections.append("")

            sections.append("")

        return "\n".join(sections)