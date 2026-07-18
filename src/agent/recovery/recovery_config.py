from dataclasses import dataclass


@dataclass(slots=True)
class RecoveryConfig:

    temperature: float = 0.0

    validate_recovery: bool = True

    strict_validation: bool = True

    max_recovery_attempts: int = 3

    verbose: bool = False