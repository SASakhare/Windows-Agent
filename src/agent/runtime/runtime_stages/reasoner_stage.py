from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stages.runtime_stage import RuntimeStage


class ReasonerStage(RuntimeStage):
    """
    Runtime stage responsible for Reasoning about our Agent Environment & give the guidance to the planner.

    Responsibilities
    ----------------
    - Invoke the Reasoner.
    - Store ReasonerOutput in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Reasoner"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        reasoner_output = context.reasoner.reason(context.state)

        context.reasoner_output = reasoner_output