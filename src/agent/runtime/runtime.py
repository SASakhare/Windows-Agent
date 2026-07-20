from src.agent.runtime.runtime_pipeline import RuntimePipeline
from src.agent.runtime.runtime_state import RuntimeState
from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_config import RuntimeConfig

from src.agent.runtime.runtime_trace import RuntimeTracer

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

        self._tracer=RuntimeTracer()

    @property
    def pipeline(self):

        return self._pipeline
    

    def run(self):

        self._tracer.start_run()

        self._runtime.running = True

        while self._runtime.running:

            self._runtime.iteration += 1
            
            self._tracer.iteration(self._runtime.iteration)

            if (
                self._runtime.iteration
                > self._config.max_iterations
            ):
                break

            for stage in self._pipeline.stages:

                self._runtime.current_stage = stage.name

                print("\n")
                print("=" * 100)
                print(f"{stage.name}")
                print("=" * 100)
                
                
                stage.execute(
                    self._context
                )

                match stage.name:

                    case "Planning":
                        self._tracer.stage(
                            "Planning",
                            self._context.state.planning,
                        )

                    case "Execution":
                        self._tracer.stage(
                            "Execution",
                            self._context.state.execution,
                        )

                    case "Observation":
                        self._tracer.stage(
                            "Observation",
                            self._context.observation_result,
                        )

                        self._tracer.stage(
                            "World State",
                            self._context.state.world,
                        )

                    case "Reflection":
                        self._tracer.stage(
                            "Reflection",
                            self._context.state.reflection,
                        )

                    case "Recovery":
                        self._tracer.stage(
                            "Recovery",
                            self._context.state.recovery,
                        )

            if (
                self._context.state.planning.goal_completed
            ):
                break

        self._runtime.running = False