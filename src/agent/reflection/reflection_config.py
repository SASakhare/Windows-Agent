from dataclasses import dataclass


@dataclass(slots=True)
class ReflectionConfig:
    """
    Configuration for the Reflection node.
    """

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    temperature: float = 0.0

    max_retries: int = 2

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validate_reflection: bool = True

    strict_validation: bool = True

    minimum_confidence: float = 0.5

    # ---------------------------------------------------------
    # Reflection
    # ---------------------------------------------------------

    detect_agent_loops: bool = True

    detect_goal_completion: bool = True

    detect_progress: bool = True

    # ---------------------------------------------------------
    # Debug
    # ---------------------------------------------------------

    verbose: bool = False

    save_prompt: bool = False

    save_reflection: bool = False