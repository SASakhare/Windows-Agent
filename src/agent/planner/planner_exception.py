class PlannerException(Exception):
    """
    Base planner exception.
    """

    pass


class PlannerValidationError(
    PlannerException,
):
    pass


class PlannerLLMError(
    PlannerException,
):
    pass
