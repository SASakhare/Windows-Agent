class ExecutorError(Exception):
    """
    Base exception for all executor-related errors.
    """

    pass


class ExecutionValidationError(ExecutorError):
    """
    Raised when PlannerOutput fails validation.
    """

    pass


class ToolNotFoundError(ExecutionValidationError):
    """
    Raised when the requested tool does not exist.
    """

    pass


class ActionNotFoundError(ExecutionValidationError):
    """
    Raised when the requested action is not supported
    by the selected tool.
    """

    pass


class MissingArgumentError(ExecutionValidationError):
    """
    Raised when one or more required arguments
    are missing.
    """

    pass


class InvalidArgumentError(ExecutionValidationError):
    """
    Raised when an argument has an invalid value
    or incorrect type.
    """

    pass


class ToolExecutionError(ExecutorError):
    """
    Raised when the tool itself fails during execution.
    """

    pass


class ExecutionTimeoutError(ExecutorError):
    """
    Raised when execution exceeds the configured timeout.
    """

    pass