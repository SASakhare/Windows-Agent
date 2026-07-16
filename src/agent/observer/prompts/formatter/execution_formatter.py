from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.execution_state import ExecutionState


class ExecutionFormatter(BaseFormatter):
    """
    Formats the current execution state for LLM consumption.
    """

    def format(   # type: ignore
        self,
        state: ExecutionState,
    ) -> str:

        result = []

        result.append("=" * 60)
        result.append("EXECUTION")
        result.append("=" * 60)

        result.append("")

        result.append(f"Status : {state.execution_status.value}")

        result.append(f"Tool : {state.active_tool or 'None'}")

        result.append(f"Action : {state.active_action or 'None'}")

        result.append("")

        result.append("Tool Result")
        result.append("-----------")

        if state.tool_result is None:

            result.append("None")

        else:

            result.append(
                f"Success : {state.tool_result.success}"
            )

            result.append(
                f"Tool : {state.tool_result.tool}"
            )

            result.append(
                f"Action : {state.tool_result.action}"
            )

            result.append("")

            result.append("Result")

            result.append(str(state.tool_result.result))

            result.append("")

            result.append("Error")

            result.append(str(state.tool_result.error))

        result.append("")

        result.append(f"Execution Time : {state.execution_time:.3f}s")

        result.append(f"Retry Count : {state.retry_count}")

        return "\n".join(result)