from src.agent.prompts.builder.base_prompt_builder import BasePromptBuilder
from src.agent.prompts.templates.recovery_template import SYSTEM_PROMPT
from src.agent.state.agent_state import AgentState


class RecoveryPromptBuilder(BasePromptBuilder):

    def __init__(
        self,
        conversation_formatter,
        planning_formatter,
        execution_formatter,
        reflection_formatter,
        recovery_formatter,
        world_formatter,
        memory_formatter,
        metadata_formatter,
    ):

        self.conversation_formatter = conversation_formatter
        self.planning_formatter = planning_formatter
        self.execution_formatter = execution_formatter
        self.reflection_formatter = reflection_formatter
        self.recovery_formatter = recovery_formatter
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

        reflection = f"""
============================================================
REFLECTION STATE
============================================================

Reflection summarizes the outcome of the previous execution.

Use this as the primary reasoning source when selecting the
next recovery strategy.

{self.reflection_formatter.format(state.reflection)}
"""

        recovery = f"""
============================================================
CURRENT RECOVERY STATE
============================================================

This section contains the current recovery history.

Use it to avoid repeated recovery loops and to understand
previous recovery attempts.

{self.recovery_formatter.format(state.recovery)}
"""

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

This is the agent's current understanding of the world.

Use it only as supporting context for selecting the recovery
strategy.

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
                reflection,
                recovery,
                conversation,
                world,
                memory,
                metadata,
            ]
        )