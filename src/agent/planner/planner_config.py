from dataclasses import dataclass


@dataclass(slots=True)
class PlannerConfig:
    """
    Configuration for the planner.
    """

    max_retries: int = 3

    validate_actions: bool = True

    publish_events: bool = True
