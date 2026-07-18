from langchain_core.language_models.chat_models import BaseChatModel

from src.agent.llm.base_llm import BaseLLM
from src.agent.prompts.builder.recovery_prompt_builder import (
    RecoveryPromptBuilder,
)

from src.agent.recovery.models.recovery_result import (
    RecoveryResult,
)

from src.agent.recovery.recovery_config import RecoveryConfig
from src.agent.recovery.recovery_validator import RecoveryValidator

from src.agent.state.agent_state import AgentState


class Recovery:

    def __init__(
        self,
        llm: BaseLLM,
        prompt_builder: RecoveryPromptBuilder,
        validator: RecoveryValidator,
        config: RecoveryConfig,
    ):

        self.config = config
        self.prompt_builder = prompt_builder
        self.validator = validator

        self.llm = llm

    def recover(
        self,
        state: AgentState,
    ) -> RecoveryResult:
        """
        Determine the safest recovery strategy after
        Reflection has evaluated the previous execution.
        """

        prompt = self.prompt_builder.build(state)

        recovery = self.llm.generate_structured(prompt,RecoveryResult)

        if self.config.validate_recovery:
            recovery = self.validator.validate(
                recovery # type: ignore
            )

        self._update_state(
            state,
            recovery, # type: ignore
        )

        return recovery # type: ignore

    def _update_state(
        self,
        state: AgentState,
        recovery: RecoveryResult,
    ) -> None:
        """
        Persist the recovery decision.
        """

        state.recovery.strategy = recovery.strategy

        state.recovery.fallback_tool = (
            recovery.fallback_tool
        )

        state.recovery.reason = recovery.reason

        state.recovery.summary = recovery.summary

        state.recovery.confidence = (
            recovery.confidence
        )

        state.recovery.verified = True

        if recovery.strategy != recovery.strategy.NONE:
            state.recovery.recovery_attempts += 1

        if recovery.reason:
            state.recovery.last_failure = recovery.reason

