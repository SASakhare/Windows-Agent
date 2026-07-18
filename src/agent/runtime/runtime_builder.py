from src.agent.events.event_bus import EventBus

from src.agent.executor.executor import Executor

from src.agent.executor.validator import ExecutionValidator
from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory

from src.agent.planner.planner import Planner

from src.agent.prompts.builder.recovery_prompt_builder import RecoveryPromptBuilder
from src.agent.prompts.builder.reflection_prompt_builder import ReflectionPromptBuilder
from src.agent.prompts.formatter.recovery_formatter import RecoveryFormatter
from src.agent.prompts.formatter.reflection_formatter import ReflectionFormatter
from src.agent.recovery.recovery import Recovery
from src.agent.recovery.recovery_config import RecoveryConfig
from src.agent.recovery.recovery_validator import RecoveryValidator
from src.agent.reflection.reflection import Reflection
from src.agent.reflection.reflection_config import ReflectionConfig
from src.agent.reflection.reflection_validator import ReflectionValidator
from src.agent.runtime.observation_stage import ObservationStage
from src.agent.runtime.reflection_stage import ReflectionStage
from src.agent.runtime.runtime import AgentRuntime
from src.agent.runtime.runtime_context import RuntimeContext

from src.agent.runtime.planning_stage import PlanningStage
from src.agent.runtime.execution_stage import ExecutionStage

from src.agent.state.agent_state import AgentState

from src.agent.tools.registry import ToolRegistry

from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.windows.file_manager import FileManagerTool
from src.agent.tools.windows.network import NetworkTool
from src.agent.tools.reasoning.reasoning_tool import ReasoningTool

from src.agent.observer.observer import Observer
from src.agent.observer.observer_config import ObserverConfig
from src.agent.observer.observation_validator import ObservationValidator
from src.agent.observer.world_updater import WorldUpdater

from src.agent.prompts.builder.observer_prompt_builder import (
    ObserverPromptBuilder,
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


def build_runtime() -> AgentRuntime:

    # --------------------------------------------------
    # Shared Infrastructure
    # --------------------------------------------------

    state = AgentState()

    event_bus = EventBus()

    registry = ToolRegistry()

    registry.register(BrowserTool)
    registry.register(FileManagerTool)
    registry.register(NetworkTool)
    registry.register(ReasoningTool)

    llm = LLMFactory.create(
        LLMConfig(
            provider="ollama",
            model_name="qwen3:14b",
        )
    )

    #^ --------------------------------------------------
    #^ Core Components
    #^ --------------------------------------------------

    # *---------------------- Planner ------------------------------
    planner = Planner(
        llm=llm,
        state=state,
        tool_registry=registry,
        event_bus=event_bus,
    )

    # *---------------------- Executor -----------------------------
    executor = Executor(
        state=state,
        tool_registry=registry,
        event_bus=event_bus,
        validator=ExecutionValidator(tool_registry=registry),
    )


    # *------------------- Observer --------------------------------
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

    # *------------------ Reflection -------------------------------
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

    # *------------------- Recovery ---------------------------------
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

    #^ --------------------------------------------------
    #^ Runtime Context
    #^ --------------------------------------------------

    context = RuntimeContext(
        state=state,
        planner=planner,
        executor=executor,
        observer=observer,
        reflection=reflection,
        recovery=recovery,
        event_bus=event_bus,
    )
    #^ --------------------------------------------------
    #^ Runtime
    #^ --------------------------------------------------

    runtime = AgentRuntime(context)

    runtime.pipeline.add_stage(PlanningStage())

    runtime.pipeline.add_stage(ExecutionStage())

    runtime.pipeline.add_stage(ObservationStage())

    runtime.pipeline.add_stage(ReflectionStage())
    
    return runtime
