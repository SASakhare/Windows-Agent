from dataclasses import dataclass


@dataclass(slots=True)
class ExecutorConfig:
    """
    Configuration for the Executor.

    Attributes
    ----------
    timeout:
        Maximum execution time (seconds) allowed for a tool.

    max_retries:
        Maximum number of retries for recoverable failures.

    raise_on_error:
        If True, executor re-raises exceptions after updating state.
        If False, returns a failed ToolResult.

    publish_events:
        Whether execution events should be published to the EventBus.

    validate_before_execution:
        Validate PlannerOutput before executing the tool.
    """

    timeout: float = 60.0

    max_retries: int = 0

    raise_on_error: bool = False

    publish_events: bool = True

    validate_before_execution: bool = True