from src.agent.prompts.builder.base_prompt_builder import BasePromptBuilder
from src.agent.prompts.templates.reflection_template import SYSTEM_PROMPT
from src.agent.state.agent_state import AgentState


class ReflectionPromptBuilder(BasePromptBuilder):

    def __init__(
        self,
        conversation_formatter,
        planning_formatter,
        execution_formatter,
        world_formatter,
        memory_formatter,
        metadata_formatter,
    ):

        self.conversation_formatter = conversation_formatter
        self.planning_formatter = planning_formatter
        self.execution_formatter = execution_formatter
        self.world_formatter = world_formatter
        self.memory_formatter = memory_formatter
        self.metadata_formatter = metadata_formatter

    def build(  # type: ignore
        self,
        state: AgentState,
    ) -> str:

        goal = f"""
============================================================
USER GOAL
============================================================

{state.goal.user_goal}
"""

        planning = self.planning_formatter.format(
            state.planning
        )

        execution = self.execution_formatter.format(
            state.execution
        )

        conversation = f"""
============================================================
CONVERSATION
============================================================

Conversation history provides context about the user's
intent and previous interactions.

{self.conversation_formatter.format(state.conversation)}
"""

        world = f"""
============================================================
WORLD STATE
============================================================

This is the current world state produced by the Observer after
the latest execution.

Use this information to determine whether progress was made,
whether the goal is complete, whether replanning is needed,
or whether the agent is stuck.

{self.world_formatter.format(state.world)}
"""

        memory = f"""
============================================================
MEMORY
============================================================

{self.memory_formatter.format(state.memory)}
"""

        metadata = f"""
============================================================
METADATA
============================================================

{self.metadata_formatter.format(state.metadata)}
"""

        return "\n\n".join(
            [
                SYSTEM_PROMPT,
                goal,
                planning,
                execution,
                conversation,
                world,
                memory,
                metadata,
            ]
        )