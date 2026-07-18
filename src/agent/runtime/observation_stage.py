from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stage import RuntimeStage


class ObservationStage(RuntimeStage):
    """
    Runtime stage responsible for observing the result of the
    previous execution.

    Responsibilities
    ----------------
    - Invoke the Observer.
    - Store ObservationResult in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Observation"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        observation = context.observer.observe()

        context.observation_result = observation