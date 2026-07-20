from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stages.runtime_stage import RuntimeStage


class RecoveryStage(RuntimeStage):
    """
    Runtime stage responsible for determining the next recovery
    strategy after reflection.

    Responsibilities
    ----------------
    - Invoke the Recovery node.
    - Store RecoveryResult in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Recovery"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        recovery = context.recovery.recover(
            context.state
        )

        context.recovery_result = recovery