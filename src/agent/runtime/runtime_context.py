from dataclasses import dataclass

from src.agent.events.event_bus import EventBus

from src.agent.planner.planner import Planner
from src.agent.planner.planner_output import PlannerOutput

from src.agent.executor.executor import Executor
from src.agent.observer.observer import Observer
from src.agent.reflection.reflection import Reflection
from src.agent.recovery.recovery import Recovery
from src.agent.observer.models.observer_result import ObserverResult
from src.agent.reflection.models.reflection_result import ReflectionResult
from src.agent.recovery.models.recovery_result import RecoveryResult

from src.agent.state.agent_state import AgentState
from src.agent.tools.tool_result import ToolResult

from src.agent.reasoner.reasoner import Reasoner
from src.agent.reasoner.reasoner_output import ReasonerOutput

@dataclass(slots=True)
class RuntimeContext:
    """
    Shared context passed between all runtime stages.

    Each stage reads the information it needs and stores its
    output back into this context.
    """

    # ==========================================================
    # Shared Agent State
    # ==========================================================

    state: AgentState

    # ==========================================================
    # Core Components
    # ==========================================================

    reasoner:Reasoner

    planner: Planner

    executor: Executor

    observer: Observer

    reflection: Reflection

    recovery: Recovery

    event_bus: EventBus

    # ==========================================================
    # Runtime Outputs
    # ==========================================================

    reasoner_output:ReasonerOutput | None= None

    planner_output: PlannerOutput | None = None

    tool_result: ToolResult | None = None

    observation_result: ObserverResult | None = None

    reflection_result: ReflectionResult | None = None

    recovery_result: RecoveryResult | None = None