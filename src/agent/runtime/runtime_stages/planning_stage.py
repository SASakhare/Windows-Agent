from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stages.runtime_stage import RuntimeStage


class PlanningStage(RuntimeStage):
    """
    Runtime stage responsible for planning the next action.

    Responsibilities
    ----------------
    - Invoke the Planner.
    - Store PlannerOutput in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Planning"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        planner_output = context.planner.plan()

        context.planner_output = planner_output