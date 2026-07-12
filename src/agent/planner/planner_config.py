from dataclasses import dataclass


@dataclass
class PlannerConfig:

    model: str = "gpt-5.5"

    temperature: float = 0.2

    max_tokens: int = 500
