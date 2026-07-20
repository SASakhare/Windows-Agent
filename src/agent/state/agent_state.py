from dataclasses import dataclass, field

from src.agent.state.context_state import ContextState
from src.agent.state.conversation_state import ConversationState
from src.agent.state.execution_state import ExecutionState
from src.agent.state.goal_state import GoalState
from src.agent.state.memory_state import MemoryState
from src.agent.state.metadata_state import MetadataState
from src.agent.state.planning_state import PlanningState
from src.agent.state.reasoner_state import ReasonerState
from src.agent.state.recovery_state import RecoveryState
from src.agent.state.reflection_state import ReflectionState
from src.agent.state.word_state import WorldState


@dataclass
class AgentState:
    """
    Central state shared across the entire agent workflow.

    Every node in the workflow reads from and writes to this object.

    Planner            -> PlanningState
    Executor           -> ExecutionState
    Observer           -> WorldState
    Reflection         -> ReflectionState
    Recovery           -> RecoveryState
    ConversationMgr    -> ConversationState
    MemoryManager      -> MemoryState
    ContextBuilder     -> ContextState
    """

    goal: GoalState = field(default_factory=GoalState)

    reasoner:ReasonerState =field(default_factory=ReasonerState)

    planning: PlanningState = field(default_factory=PlanningState)

    execution: ExecutionState = field(default_factory=ExecutionState)

    world: WorldState = field(default_factory=WorldState)

    memory: MemoryState = field(default_factory=MemoryState)

    conversation: ConversationState = field(default_factory=ConversationState)

    reflection: ReflectionState = field(default_factory=ReflectionState)

    recovery: RecoveryState = field(default_factory=RecoveryState)

    context: ContextState = field(default_factory=ContextState)

    metadata: MetadataState = field(default_factory=MetadataState)