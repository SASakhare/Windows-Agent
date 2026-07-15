from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeState:

    running: bool = False

    iteration: int = 0

    current_stage: str | None = None

    last_error: str | None = None