from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeConfig:

    max_iterations: int = 20

    stop_on_error: bool = True

    publish_events: bool = True