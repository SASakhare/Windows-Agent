from src.agent.prompts.builder.base_prompt_builder import BasePromptBuilder
from src.agent.prompts.templates.planner_template import SYSTEM_PROMPT
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry


class PlannerPromptBuilder(BasePromptBuilder):

    def __init__(
        self,
        tool_formatter,
        conversation_formatter,
        reasoner_formatter,
        planning_formatter,
        execution_formatter,
        world_formatter,
    ) -> None:

        self.tool_formatter = tool_formatter
        self.conversation_formatter = conversation_formatter
        self.reasoner_formatter = reasoner_formatter
        self.planning_formatter = planning_formatter
        self.execution_formatter = execution_formatter
        self.world_formatter = world_formatter

    def build(  # type: ignore
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
REASONER GUIDANCE
============================================================

The Reasoner has already analyzed the user's objective,
the current environment, previous progress,
and determined the overall strategy.

Follow this guidance when selecting the next action.

{self.reasoner_formatter.format(state.reasoner)}
""",

            f"""
============================================================
CURRENT PLAN
============================================================

This is the planner's previous action.

Avoid repeating actions that have already succeeded.

{self.planning_formatter.format(state.planning)}
""",

            f"""
============================================================
LAST EXECUTION
============================================================

This is the result of the previously executed action.

Use it to determine whether the next action should change.

{self.execution_formatter.format(state.execution)}
""",

            f"""
============================================================
WORLD STATE
============================================================

The World State represents the agent's current understanding
of the environment.

Always use this information before selecting the next action.

Do not repeat successful actions.

{self.world_formatter.format(state.world)}
""",

            f"""
============================================================
CONVERSATION
============================================================

The conversation history may contain references,
clarifications, or additional user constraints.

{self.conversation_formatter.format(state.conversation)}
""",

            f"""
============================================================
AVAILABLE TOOLS
============================================================

Only use the tools listed below.

Each tool contains:

• Purpose

• Available Actions

• Required Arguments

Choose the tool that best satisfies the
Reasoner's guidance.

{self.tool_formatter.format(tool_registry)}
"""
        ]

        return "\n\n".join(sections)