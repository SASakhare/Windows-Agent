from dataclasses import dataclass

from src.agent.planner.planner_output import PlannerOutput
from src.agent.state.agent_state import AgentState


@dataclass(slots=True)
class ObserverContext:

    planner_output: PlannerOutput

    state: AgentState