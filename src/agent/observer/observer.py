import time

from src.agent.events.event_bus import EventBus
from src.agent.llm.base_llm import BaseLLM
from src.agent.observer.models.observation import Observation
from src.agent.observer.models.observer_result import ObserverResult
from src.agent.observer.observation_validator import ObservationValidator
from src.agent.observer.observer_config import ObserverConfig
from src.agent.observer.world_updater import WorldUpdater
from src.agent.prompts.builder.observer_prompt_builder import (
    ObserverPromptBuilder,
)
from src.agent.state.agent_state import AgentState


class Observer:
    """
    Observer Node

    Responsibilities
    ----------------
    1. Build the observation prompt.
    2. Ask the LLM to analyse the execution.
    3. Validate the generated Observation.
    4. Update the World State.
    5. Return an ObserverResult.
    """

    def __init__(
        self,
        llm: BaseLLM,
        state: AgentState,
        prompt_builder: ObserverPromptBuilder,
        validator: ObservationValidator,
        world_updater: WorldUpdater,
        event_bus: EventBus,
        config: ObserverConfig,
    ) -> None:

        self._llm = llm
        self._state = state
        self._prompt_builder = prompt_builder
        self._validator = validator
        self._world_updater = world_updater
        self._event_bus = event_bus
        self._config = config

    # ---------------------------------------------------------

    def observe(self) -> ObserverResult:

        start = time.perf_counter()

        # -----------------------------------------------------
        # Build Prompt
        # -----------------------------------------------------

        prompt = self._prompt_builder.build(
            self._state,
        )

        # -----------------------------------------------------
        # LLM Observation
        # -----------------------------------------------------

        observation: Observation = self._llm.generate_structured(
            prompt=prompt,
            schema=Observation,
        ) # type: ignore

        print(observation);

        # -----------------------------------------------------
        # Validate
        # -----------------------------------------------------

        if self._config.validate_observation:

            self._validator.validate(
                observation,
            )

        # -----------------------------------------------------
        # Update World State
        # -----------------------------------------------------

        world_updated = False

        if self._config.update_world_state:

            self._world_updater.update(
                self._state.world,
                observation,
            )

            world_updated = True

        elapsed = time.perf_counter() - start

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        return ObserverResult(
            observation=observation,
            world_updated=world_updated,
            execution_time=elapsed,
        )