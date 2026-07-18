from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stage import RuntimeStage


class ReflectionStage(RuntimeStage):
    """
    Runtime stage responsible for evaluating the latest execution.

    Responsibilities
    ----------------
    - Invoke the Reflection node.
    - Store ReflectionResult in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Reflection"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        reflection = context.reflection.reflect(
            context.state
        )

        context.reflection_result = reflection