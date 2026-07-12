from dataclasses import dataclass

from src.agent.models.action import Action

@dataclass(slots=True)
class PlannerResult:

    '''
    Result returned by the Planner.
    '''

    thought:str

    action:Action

    goal_completed:bool = False

















