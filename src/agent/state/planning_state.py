from dataclasses import dataclass,field
from typing import List

from src.agent.models.action import Action


@dataclass
class PlanningState:

    plan:List[str] = field(default_factory=list)  # ^ Not the complete plan,think of it as the remaining plan

    current_action:Action|None=None # ^ The action Executor is executing

    next_action:str="" # ^ Next action 

    planner_reasoning:str="" # ^ short explanation about why this action is happening

    expected_outcome:str="" # ^ what is the expected output after execution of this action

    goal_completed:bool=False




















