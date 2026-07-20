from src.agent.runtime.runtime_context import RuntimeContext
from src.agent.runtime.runtime_stages.runtime_stage import RuntimeStage


class ExecutionStage(RuntimeStage):
    """
    Runtime stage responsible for executing the PlannerOutput.

    Responsibilities
    ----------------
    - Read PlannerOutput from RuntimeContext.
    - Execute the action.
    - Store ToolResult in RuntimeContext.
    """

    @property
    def name(self) -> str:
        return "Execution"

    def execute(
        self,
        context: RuntimeContext,
    ) -> None:

        if context.planner_output is None:
            raise RuntimeError(
                "PlannerOutput not found. "
                "PlanningStage must run before ExecutionStage."
            )

        tool_result = context.executor.execute(
            context.planner_output
        )

        context.tool_result = tool_result