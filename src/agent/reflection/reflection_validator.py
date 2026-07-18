from src.agent.reflection.models.reflection_result import ReflectionResult


class ReflectionValidator:
    """
    Validates the Reflection node output.

    Ensures the ReflectionResult is internally consistent
    before it is stored in the agent state.
    """

    def validate(self, reflection: ReflectionResult) -> ReflectionResult:

        self._validate_confidence(reflection)
        self._validate_goal_completion(reflection)
        self._validate_replanning(reflection)
        self._validate_summary(reflection)

        return reflection

    # ---------------------------------------------------------
    # Private Validators
    # ---------------------------------------------------------

    def _validate_confidence(
        self,
        reflection: ReflectionResult,
    ) -> None:

        if not 0.0 <= reflection.confidence <= 1.0:
            raise ValueError("Reflection confidence must be between 0 and 1.")

    def _validate_goal_completion(
        self,
        reflection: ReflectionResult,
    ) -> None:

        if reflection.goal_completed and reflection.needs_replanning:
            raise ValueError("Goal cannot be completed while replanning is required.")

    def _validate_replanning(
        self,
        reflection: ReflectionResult,
    ) -> None:

        if reflection.agent_stuck and not reflection.needs_replanning:
            raise ValueError("A stuck agent should require replanning.")

    def _validate_summary(
        self,
        reflection: ReflectionResult,
    ) -> None:

        if not reflection.summary.strip():
            raise ValueError("Reflection summary cannot be empty.")
