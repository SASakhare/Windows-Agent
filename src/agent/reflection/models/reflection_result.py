from pydantic import BaseModel, Field


class ReflectionResult(BaseModel):
    """
    Structured output returned by the Reflection LLM.
    """

    progress_made: bool = Field(
        description="Whether the previous action moved the agent closer to the user's goal."
    )

    goal_completed: bool = Field(
        description="Whether the user's goal has been achieved."
    )

    needs_replanning: bool = Field(
        description="Whether the Planner should generate a new plan."
    )

    failure_detected: bool = Field(
        description="Whether a meaningful failure occurred."
    )

    agent_stuck: bool = Field(
        description="Whether the agent appears stuck in a repeated loop."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence of this reflection."
    )

    reason: str = Field(
        description="Why this conclusion was reached."
    )

    summary: str = Field(
        description="Short summary for future planning."
    )