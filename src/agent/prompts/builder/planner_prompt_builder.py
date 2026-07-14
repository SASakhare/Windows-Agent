from src.agent.prompts.builder.base_prompt_builder import BasePromptBuilder
from src.agent.prompts.templates.planner_template import SYSTEM_PROMPT
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry


class PlannerPromptBuilder(BasePromptBuilder):

    def __init__(
        self,
        tool_formatter,
        conversation_formatter,
        planning_formatter,
        world_formatter,
    ):

        self.tool_formatter = tool_formatter

        self.conversation_formatter = conversation_formatter

        self.planning_formatter = planning_formatter

        self.world_formatter = world_formatter

    def build(  # type: ignore
        self,
        state: AgentState,
        tool_registry: ToolRegistry,
    ) -> str:

        goal = f"""
============================================================
USER GOAL
============================================================

{state.goal.user_goal}
"""

        planning = self.planning_formatter.format(state.planning)

        conversation = f"""
============================================================
CONVERSATION
============================================================

The conversation history helps identify the user's intent,
previous clarifications, and preferences.

{self.conversation_formatter.format(state.conversation)}
"""

        world = f"""
============================================================
WORLD STATE
============================================================

The World State represents the agent's current understanding
of the environment.

Use it to avoid unnecessary or repeated actions.

{self.world_formatter.format(state.world)}
    """

        tools = f"""
============================================================
AVAILABLE TOOLS
============================================================

Only use the tools listed below.

Each tool contains its purpose, available actions,
and required arguments.

{self.tool_formatter.format(tool_registry)}
"""

        return "\n\n".join(
            [
                SYSTEM_PROMPT,
                goal,
                planning,
                conversation,
                world,
                tools,
            ]
        )
