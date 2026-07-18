# src/agent/reflection/test.py

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

from src.agent.prompts.formatter.word_formatter import WorldFormatter

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
print("EXECUTION STATE")
print("=" * 100)
print(state.execution)


# ============================================================
# Observer Prompt Builder
# ============================================================

observer_prompt_builder = ObserverPromptBuilder(
    conversation_formatter=ConversationFormatter(),
    planning_formatter=PlanningFormatter(),
    execution_formatter=ExecutionFormatter(),
    world_formatter=WorldFormatter(),
    memory_formatter=MemoryFormatter(),
    metadata_formatter=MetadataFormatter(),
)


# ============================================================
# Observer
# ============================================================

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


# ============================================================
# Print Observation
# ============================================================

print("\n")
print("=" * 100)
print("OBSERVATION RESULT")
print("=" * 100)

print(observer_result.observation)


# ============================================================
# Print World State
# ============================================================

print("\n")
print("=" * 100)
print("WORLD STATE")
print("=" * 100)

print(state.world)


# ============================================================
# Reflection Prompt Builder
# ============================================================

reflection_prompt_builder = ReflectionPromptBuilder(
    conversation_formatter=ConversationFormatter(),
    planning_formatter=PlanningFormatter(),
    execution_formatter=ExecutionFormatter(),
    world_formatter=WorldFormatter(),
    memory_formatter=MemoryFormatter(),
    metadata_formatter=MetadataFormatter(),
)


# ============================================================
# Reflection
# ============================================================

reflection = Reflection(
    llm=llm, # type: ignore
    prompt_builder=reflection_prompt_builder,
    validator=ReflectionValidator(),
    config=ReflectionConfig(),
)

reflection_result = reflection.reflect(state)


# ============================================================
# Reflection Result
# ============================================================

print("\n")
print("=" * 100)
print("REFLECTION RESULT")
print("=" * 100)

print(f"Progress Made     : {reflection_result.progress_made}")
print(f"Goal Completed    : {reflection_result.goal_completed}")
print(f"Needs Replanning  : {reflection_result.needs_replanning}")
print(f"Failure Detected  : {reflection_result.failure_detected}")
print(f"Agent Stuck       : {reflection_result.agent_stuck}")
print(f"Confidence        : {reflection_result.confidence}")
print(f"Reason            : {reflection_result.reason}")
print(f"Summary           : {reflection_result.summary}")


# ============================================================
# Reflection State
# ============================================================

print("\n")
print("=" * 100)
print("REFLECTION STATE")
print("=" * 100)

print(state.reflection)