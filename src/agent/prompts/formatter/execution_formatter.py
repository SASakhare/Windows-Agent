from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.execution_state import ExecutionState


class ExecutionFormatter(BaseFormatter):

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
        result.append(f"Active Tool : {state.active_tool or 'None'}")
        result.append(f"Active Action : {state.active_action or 'None'}")
        result.append(f"Retry Count : {state.retry_count}")
        result.append(
            f"Execution Time : {state.execution_time:.3f}s"
        )

        result.append("")
        result.append("TOOL RESULT")
        result.append("-" * 20)

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

            # result.append("Arguments:")
            # result.append(str(state.tool_result.arguments))

            result.append("Result:")
            result.append(str(state.tool_result.result))

            result.append("Error:")
            result.append(str(state.tool_result.error))

        return "\n".join(result)