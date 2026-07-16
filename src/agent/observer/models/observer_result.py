from pydantic import BaseModel

from src.agent.observer.models.observation import Observation


class ObserverResult(BaseModel):
    """
    Output returned by the Observer component.
    """

    observation: Observation

    world_updated: bool

    execution_time: float