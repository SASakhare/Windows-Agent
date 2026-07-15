from src.agent.planner.planner_output import PlannerOutput
from src.agent.tools.registry import ToolRegistry
from src.agent.executor.exceptions import (
    ToolNotFoundError,
    ActionNotFoundError,
    MissingArgumentError,
)

class ExecutionValidator:
    """
    Validates PlannerOutput before execution.

    Responsibilities
    ----------------
    - Validate tool exists.
    - Validate action exists.
    - Validate required arguments.
    """

    def __init__(
        self,
        tool_registry: ToolRegistry,
    ) -> None:

        self._tool_registry = tool_registry

    def validate(
        self,
        planner_output: PlannerOutput,
    ) -> None:
        """
        Raises ValueError if the planner output is invalid.
        """

        action = planner_output.action

        self._validate_tool(action.tool)

        schema = self._tool_registry.get_schema(
            action.tool
        )

        action_schema = self._validate_action(
            schema,
            action.action,
        )

        self._validate_arguments(
            action.arguments,
            action_schema,
        )

    # ---------------------------------------------------------

    def _validate_tool(
        self,
        tool_name: str,
    ) -> None:

        if tool_name not in self._tool_registry.get_all_schemas():

            raise ToolNotFoundError(
                f"Unknown tool '{tool_name}'."
            )

    # ---------------------------------------------------------

    def _validate_action(
        self,
        tool_schema: dict,
        action_name: str,
    ) -> dict:

        for action in tool_schema["actions"]:

            if action["name"] == action_name:

                return action

        raise ActionNotFoundError(
            f"Unknown action '{action_name}'."
        )

    # ---------------------------------------------------------

    def _validate_arguments(
        self,
        arguments: dict,
        action_schema: dict,
    ) -> None:

        parameters = action_schema["parameters"]

        for name, info in parameters.items():

            if (
                info["required"]
                and name not in arguments
            ):

                raise MissingArgumentError(
                    f"Missing required argument '{name}'."
                )