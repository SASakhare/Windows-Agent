from src.agent.events.event_bus import EventBus
from src.agent.models.planner_result import PlannerResult
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry


class Planner:

    def __init__(
        self,
        llm,
        state: AgentState,
        tool_registry: ToolRegistry,
        event_bus: EventBus,
    ):

        ...

    #^ ==============================
    #^ Public API
    #^ ==============================

    def plan(self) -> PlannerResult:
        ...

    #^ ==============================
    #^ Internal
    #^ ==============================

    def _build_prompt(self) -> str:
        ...

    def _call_llm(self, prompt: str) -> str:
        ...

    def _parse(self, response: str) -> PlannerResult:
        ...

    def _validate(self, result: PlannerResult) -> None:
        ...

    def _update_state(self, result: PlannerResult) -> None:
        ...

    def _publish_event(self, result: PlannerResult) -> None:
        ...