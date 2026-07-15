from dataclasses import dataclass

from src.agent.events.event_bus import EventBus

from src.agent.planner.planner import Planner
from src.agent.planner.planner_output import PlannerOutput
from src.agent.executor.executor import Executor

from src.agent.state.agent_state import AgentState
from src.agent.tools.tool_result import ToolResult

@dataclass(slots=True)
class RuntimeContext:

    state: AgentState

    planner: Planner

    executor: Executor

    event_bus: EventBus

    planner_output :PlannerOutput | None = None

    tool_result:ToolResult | None = None