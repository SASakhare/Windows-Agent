from src.agent.runtime.runtime_pipeline import RuntimePipeline
from src.agent.runtime.runtime_state import RuntimeState
from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_config import RuntimeConfig


class AgentRuntime:

    """
    Coordinates all runtime stages.

    Runtime owns the execution loop.

    Stages perform the work.
    """

    def __init__(
        self,
        context: RuntimeContext,
        config: RuntimeConfig | None = None,
    ):

        self._context = context

        self._config = config or RuntimeConfig()

        self._pipeline = RuntimePipeline()

        self._runtime = RuntimeState()

    @property
    def pipeline(self):

        return self._pipeline

    def run(self):

        self._runtime.running = True

        while self._runtime.running:

            self._runtime.iteration += 1

            if (
                self._runtime.iteration
                > self._config.max_iterations
            ):
                break

            for stage in self._pipeline.stages:

                self._runtime.current_stage = stage.name

                stage.execute(
                    self._context
                )

            if (
                self._context.state.goal.status
            ):
                break

        self._runtime.running = False