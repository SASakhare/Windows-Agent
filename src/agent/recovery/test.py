from src.agent.events.event_bus import EventBus

from src.agent.executor.executor import Executor
from src.agent.executor.validator import ExecutionValidator

from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory

from src.agent.messages.messages import Message, MessageRole

from src.agent.observer.observer import Observer
from src.agent.observer.observer_config import ObserverConfig
from src.agent.observer.observation_validator import ObservationValidator
from src.agent.observer.world_updater import WorldUpdater

from src.agent.planner.planner import Planner

from src.agent.prompts.builder.observer_prompt_builder import (
    ObserverPromptBuilder,
)

from src.agent.prompts.builder.reflection_prompt_builder import (
    ReflectionPromptBuilder,
)

from src.agent.prompts.builder.recovery_prompt_builder import (
    RecoveryPromptBuilder,
)

from src.agent.prompts.formatter.conversation_formatter import (
    ConversationFormatter,
)

from src.agent.prompts.formatter.execution_formatter import (
    ExecutionFormatter,
)

from src.agent.prompts.formatter.memory_formatter import (
    MemoryFormatter,
)

from src.agent.prompts.formatter.metadata_formatter import (
    MetadataFormatter,
)

from src.agent.prompts.formatter.planning_formatter import (
    PlanningFormatter,
)

from src.agent.prompts.formatter.recovery_formatter import (
    RecoveryFormatter,
)

from src.agent.prompts.formatter.reflection_formatter import ReflectionFormatter

from src.agent.prompts.formatter.word_formatter import (WorldFormatter)

from src.agent.recovery.recovery import Recovery
from src.agent.recovery.recovery_config import RecoveryConfig
from src.agent.recovery.recovery_validator import RecoveryValidator

from src.agent.reflection.reflection import Reflection
from src.agent.reflection.reflection_config import ReflectionConfig
from src.agent.reflection.reflection_validator import ReflectionValidator

from src.agent.state.agent_state import AgentState

from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.registry import ToolRegistry
from src.agent.tools.windows.file_manager import FileManagerTool
from src.agent.tools.windows.network import NetworkTool


# ============================================================
# Tool Registry
# ============================================================

tool_registry = ToolRegistry()

tool_registry.register(BrowserTool)
tool_registry.register(FileManagerTool)
tool_registry.register(NetworkTool)


# ============================================================
# Agent State
# ============================================================

state = AgentState()

state.goal.user_goal = "Open google.com"

state.conversation.conversation_history.append(
    Message(
        role=MessageRole.USER,
        content="Open google.com",
    )
)


# ============================================================
# LLM
# ============================================================

config = LLMConfig(
    provider="ollama",
    model_name="qwen3:14b",
)

llm = LLMFactory.create(config)


# ============================================================
# Event Bus
# ============================================================

event_bus = EventBus()


# ============================================================
# Planner
# ============================================================

planner = Planner(
    llm=llm,
    state=state,
    tool_registry=tool_registry,
    event_bus=event_bus,
)

planner_output = planner.plan()

print("\n")
print("=" * 100)
print("PLANNER OUTPUT")
print("=" * 100)
print(planner_output)


# ============================================================
# Executor
# ============================================================

executor = Executor(
    state=state,
    tool_registry=tool_registry,
    event_bus=event_bus,
    validator=ExecutionValidator(tool_registry),
)

executor.execute(planner_output)

print("\n")
print("=" * 100)
print("EXECUTION")
print("=" * 100)
print(state.execution)


# ============================================================
# Observer
# ============================================================

observer_prompt_builder = ObserverPromptBuilder(
    conversation_formatter=ConversationFormatter(),
    planning_formatter=PlanningFormatter(),
    execution_formatter=ExecutionFormatter(),
    world_formatter=WorldFormatter(),
    memory_formatter=MemoryFormatter(),
    metadata_formatter=MetadataFormatter(),
)

observer = Observer(
    llm=llm,
    state=state,
    prompt_builder=observer_prompt_builder,
    validator=ObservationValidator(),
    world_updater=WorldUpdater(),
    event_bus=event_bus,
    config=ObserverConfig(),
)

observer_result = observer.observe()

print("\n")
print("=" * 100)
print("OBSERVATION")
print("=" * 100)
print(observer_result.observation)


print("\n")
print("=" * 100)
print("WORLD STATE")
print("=" * 100)
print(state.world)


# ============================================================
# Reflection
# ============================================================

reflection_prompt_builder = ReflectionPromptBuilder(
    conversation_formatter=ConversationFormatter(),
    planning_formatter=PlanningFormatter(),
    execution_formatter=ExecutionFormatter(),
    world_formatter=WorldFormatter(),
    memory_formatter=MemoryFormatter(),
    metadata_formatter=MetadataFormatter(),
)

reflection = Reflection(
    llm=llm,
    prompt_builder=reflection_prompt_builder,
    validator=ReflectionValidator(),
    config=ReflectionConfig(),
)

reflection_result = reflection.reflect(state)

print("\n")
print("=" * 100)
print("REFLECTION")
print("=" * 100)
print(reflection_result)

print("\n")
print("=" * 100)
print("REFLECTION STATE")
print("=" * 100)
print(state.reflection)


# ============================================================
# Recovery
# ============================================================

recovery_prompt_builder = RecoveryPromptBuilder(
    conversation_formatter=ConversationFormatter(),
    planning_formatter=PlanningFormatter(),
    execution_formatter=ExecutionFormatter(),
    reflection_formatter=ReflectionFormatter(),
    recovery_formatter=RecoveryFormatter(),
    world_formatter=WorldFormatter(),
    memory_formatter=MemoryFormatter(),
    metadata_formatter=MetadataFormatter(),
)

recovery = Recovery(
    llm=llm,
    prompt_builder=recovery_prompt_builder,
    validator=RecoveryValidator(),
    config=RecoveryConfig(),
)

recovery_result = recovery.recover(state)


# ============================================================
# Recovery Result
# ============================================================

print("\n")
print("=" * 100)
print("RECOVERY RESULT")
print("=" * 100)

print(f"Strategy          : {recovery_result.strategy}")
print(f"Fallback Tool     : {recovery_result.fallback_tool}")
print(f"Confidence        : {recovery_result.confidence}")
print(f"Reason            : {recovery_result.reason}")
print(f"Summary           : {recovery_result.summary}")


print("\n")
print("=" * 100)
print("RECOVERY STATE")
print("=" * 100)

print(state.recovery)