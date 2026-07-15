from src.agent.events.event_bus import EventBus

from src.agent.executor.executor import Executor

from src.agent.executor.validator import ExecutionValidator
from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory

from src.agent.planner.planner import Planner

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

    # --------------------------------------------------
    # Core Components
    # --------------------------------------------------

    planner = Planner(

        llm=llm,

        state=state,

        tool_registry=registry,

        event_bus=event_bus,

    )

    executor = Executor(

        state=state,

        tool_registry=registry,

        event_bus=event_bus,

        validator=ExecutionValidator(tool_registry=registry)
    )

    # --------------------------------------------------
    # Runtime Context
    # --------------------------------------------------

    context = RuntimeContext(

        state=state,

        planner=planner,

        executor=executor,

        event_bus=event_bus,

    )

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    runtime = AgentRuntime(context)

    runtime.pipeline.add_stage(

        PlanningStage()

    )

    runtime.pipeline.add_stage(

        ExecutionStage()

    )

    return runtime