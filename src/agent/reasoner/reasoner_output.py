from pydantic import BaseModel, Field


class ReasonerOutput(BaseModel):
    """
    Structured output returned by the Reasoner.

    This model represents the agent's strategic understanding of
    the current task. It does not contain executable actions.
    """

    objective: str = Field(
        description="The user's current objective."
    )

    understanding: str = Field(
        description="A concise understanding of the current situation."
    )

    strategy: str = Field(
        description="The high-level strategy for achieving the objective."
    )

    current_focus: str = Field(
        description="The single most important thing the agent should focus on next."
    )

    planner_guidance: str = Field(
        description="High-level guidance for the Planner. Do not include executable actions."
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Assumptions currently being made."
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Known constraints that must be respected."
    )

    lessons: list[str] = Field(
        default_factory=list,
        description="Lessons learned from previous iterations."
    )

    known_failures: list[str] = Field(
        default_factory=list,
        description="Failures that should not be repeated."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the current reasoning."
    )