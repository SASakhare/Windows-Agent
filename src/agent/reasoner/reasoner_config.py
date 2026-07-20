from dataclasses import dataclass


@dataclass(slots=True)
class ReasonerConfig:
    """
    Configuration for the Reasoner.

    Controls how the Reasoner generates strategic reasoning.
    """

    model: str = "gpt-4.1"

    temperature: float = 0.2

    max_tokens: int = 1200

    top_p: float = 1.0

    max_retries: int = 3

    timeout: float = 60.0

    validate_output: bool = True

    enable_reasoning_trace: bool = False