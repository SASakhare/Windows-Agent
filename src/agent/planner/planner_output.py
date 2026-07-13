from pydantic import BaseModel, Field

from src.agent.models.action import Action


class PlannerOutput(BaseModel):
    """
    Structured output returned by the Planner LLM.
    """

    thought: str = Field(
        description="Reasoning behind choosing the next action.",
    )

    action: Action = Field(
        description="The next executable action.",
    )

    expected_outcome: str = Field(
        description="Expected result after executing the action.",
    )

    goal_completed: bool = Field(
        default=False,
        description="Whether the overall goal has been achieved.",
    )
