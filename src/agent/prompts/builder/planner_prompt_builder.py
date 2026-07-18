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
        execution_formatter,
        world_formatter,
        reflection_formatter,
        recovery_formatter,
    ) -> None:

        self.tool_formatter = tool_formatter
        self.conversation_formatter = conversation_formatter
        self.planning_formatter = planning_formatter
        self.execution_formatter = execution_formatter
        self.world_formatter = world_formatter
        self.reflection_formatter = reflection_formatter
        self.recovery_formatter = recovery_formatter

    def build( # type: ignore
        self,
        state: AgentState,
        tool_registry: ToolRegistry,
    ) -> str:

        sections = [
            SYSTEM_PROMPT,

            f"""
============================================================
USER GOAL
============================================================

{state.goal.user_goal}
""",

            f"""
============================================================
CURRENT PLAN
============================================================

This is the planner's previous reasoning and selected action.

{self.planning_formatter.format(state.planning)}
""",

            f"""
============================================================
LAST EXECUTION
============================================================

This is the result of the previously executed action.

{self.execution_formatter.format(state.execution)}
""",

            f"""
============================================================
WORLD STATE
============================================================

The World State represents the agent's current understanding
of the environment.

Always reason using this information before selecting the next
action. Do not repeat actions that have already succeeded.

{self.world_formatter.format(state.world)}
""",

            f"""
============================================================
LAST REFLECTION
============================================================

Reflection summarizes whether meaningful progress was made
towards the user's goal and identifies remaining work.

{self.reflection_formatter.format(state.reflection)}
""",

            f"""
============================================================
LAST RECOVERY
============================================================

Recovery summarizes the strategy selected after the previous
iteration (continue, retry, replan, ask user, abort, etc.).

Use this information when deciding the next action.

{self.recovery_formatter.format(state.recovery)}
""",

            f"""
============================================================
CONVERSATION
============================================================

The conversation history provides the user's intent,
clarifications, and preferences.

{self.conversation_formatter.format(state.conversation)}
""",

            f"""
============================================================
AVAILABLE TOOLS
============================================================

Only use the tools listed below.

Each tool contains:
- Purpose
- Available actions
- Required arguments

{self.tool_formatter.format(tool_registry)}
"""
        ]

        return "\n\n".join(sections)