from langchain_core.language_models.chat_models import BaseChatModel

from src.agent.llm.base_llm import BaseLLM
from src.agent.reflection.models.reflection_result import ReflectionResult
from src.agent.reflection.reflection_config import ReflectionConfig
from src.agent.reflection.reflection_validator import ReflectionValidator

from src.agent.prompts.builder.reflection_prompt_builder import (
    ReflectionPromptBuilder,
)

from src.agent.state.agent_state import AgentState


class Reflection:

    def __init__(
        self,
        llm: BaseLLM,
        prompt_builder: ReflectionPromptBuilder,
        validator: ReflectionValidator,
        config: ReflectionConfig,
    ):

        self.config = config
        self.prompt_builder = prompt_builder
        self.validator = validator

        self.llm = llm

    def reflect(
        self,
        state: AgentState,
    ) -> ReflectionResult:
        """
        Evaluate the previous execution and determine
        the next reasoning state of the agent.
        """

        prompt = self.prompt_builder.build(state)

        reflection = self.llm.generate_structured(prompt=prompt,schema=ReflectionResult)

        if self.config.validate_reflection:
            reflection = self.validator.validate(
                reflection # type: ignore
            )

        self._update_state(
            state,
            reflection, # type: ignore
        )

        return reflection # type: ignore

    def _update_state(
        self,
        state: AgentState,
        reflection: ReflectionResult,
    ) -> None:
        """
        Persist the reflection into the agent state.
        """

        state.reflection.progress_made = (
            reflection.progress_made
        )

        state.reflection.goal_completed = (
            reflection.goal_completed
        )

        state.reflection.needs_replanning = (
            reflection.needs_replanning
        )

        state.reflection.failure_detected = (
            reflection.failure_detected
        )

        state.reflection.agent_stuck = (
            reflection.agent_stuck
        )

        state.reflection.confidence = (
            reflection.confidence
        )

        state.reflection.reason = (
            reflection.reason
        )

        state.reflection.summary = (
            reflection.summary
        )

        state.reflection.verified = True