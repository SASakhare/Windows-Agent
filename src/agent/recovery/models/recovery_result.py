from pydantic import BaseModel, Field

from src.agent.state.recovery_state import RecoveryStrategy


class RecoveryResult(BaseModel):
    """
    Structured output returned by the Recovery node.
    """

    strategy: RecoveryStrategy = Field(
        description="The recovery strategy the runtime should execute."
    )

    fallback_tool: str = Field(
        default="",
        description="Fallback tool to use when strategy is FALLBACK_TOOL."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in this recovery decision."
    )

    reason: str = Field(
        description="Why this recovery strategy was selected."
    )

    summary: str = Field(
        description="Short summary for the runtime."
    )