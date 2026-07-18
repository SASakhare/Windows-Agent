from src.agent.recovery.models.recovery_result import RecoveryResult
from src.agent.state.recovery_state import RecoveryStrategy


class RecoveryValidator:
    """
    Validates RecoveryResult produced by the Recovery node.
    """

    def validate(
        self,
        recovery: RecoveryResult,
    ) -> RecoveryResult:

        self._validate_confidence(recovery)
        self._validate_strategy(recovery)
        self._validate_fallback_tool(recovery)
        self._validate_summary(recovery)

        return recovery

    # ---------------------------------------------------------
    # Private Validators
    # ---------------------------------------------------------

    def _validate_confidence(
        self,
        recovery: RecoveryResult,
    ) -> None:

        if not 0.0 <= recovery.confidence <= 1.0:
            raise ValueError(
                "Recovery confidence must be between 0 and 1."
            )

    def _validate_strategy(
        self,
        recovery: RecoveryResult,
    ) -> None:

        if recovery.strategy is None:
            raise ValueError(
                "Recovery strategy cannot be None."
            )

    def _validate_fallback_tool(
        self,
        recovery: RecoveryResult,
    ) -> None:

        if (
            recovery.strategy == RecoveryStrategy.FALLBACK_TOOL
            and not recovery.fallback_tool.strip()
        ):
            raise ValueError(
                "Fallback tool is required when strategy is FALLBACK_TOOL."
            )

        if (
            recovery.strategy != RecoveryStrategy.FALLBACK_TOOL
            and recovery.fallback_tool.strip()
        ):
            raise ValueError(
                "Fallback tool should only be specified when strategy is FALLBACK_TOOL."
            )

    def _validate_summary(
        self,
        recovery: RecoveryResult,
    ) -> None:

        if not recovery.summary.strip():
            raise ValueError(
                "Recovery summary cannot be empty."
            )