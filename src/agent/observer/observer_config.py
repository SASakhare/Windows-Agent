from dataclasses import dataclass


@dataclass(slots=True)
class ObserverConfig:
    """
    Configuration for the Observer component.
    """

    # ---------------------------------------------------------
    # LLM
    # ---------------------------------------------------------

    temperature: float = 0.0

    max_retries: int = 2

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validate_observation: bool = False

    strict_validation: bool = True

    # ---------------------------------------------------------
    # World State
    # ---------------------------------------------------------

    update_world_state: bool = True

    overwrite_existing_values: bool = False

    # ---------------------------------------------------------
    # Observation
    # ---------------------------------------------------------

    detect_mismatches: bool = True

    generate_summary: bool = True

    minimum_confidence: float = 0.5

    # ---------------------------------------------------------
    # Debug
    # ---------------------------------------------------------

    verbose: bool = False

    save_prompt: bool = False

    save_observation: bool = False

    