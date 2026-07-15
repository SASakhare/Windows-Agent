from src.agent.events.event_bus import EventBus

from src.agent.executor.executor import Executor

from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory

from src.agent.messages.messages import (
    Message,
    MessageRole,
)

from src.agent.planner.planner import Planner

from src.agent.state.agent_state import AgentState

from src.agent.tools.registry import ToolRegistry

from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.windows.file_manager import FileManagerTool
from src.agent.tools.windows.network import NetworkTool

from src.agent.executor.validator import ExecutionValidator

def main():

    # ----------------------------------------------------
    # Tool Registry
    # ----------------------------------------------------

    registry = ToolRegistry()

    registry.register(BrowserTool)
    registry.register(FileManagerTool)
    registry.register(NetworkTool)

    # ----------------------------------------------------
    # Agent State
    # ----------------------------------------------------

    state = AgentState()

    state.goal.user_goal = "Open google.com"

    state.conversation.conversation_history = [

        Message(
            role=MessageRole.USER,
            content="Open google.com",
        )

    ]

    # ----------------------------------------------------
    # Event Bus
    # ----------------------------------------------------

    bus = EventBus()

    # ----------------------------------------------------
    # LLM
    # ----------------------------------------------------

    llm = LLMFactory.create(

        LLMConfig(

            provider="ollama",

            model_name="qwen3:14b",

        )

    )

    # ----------------------------------------------------
    # Planner
    # ----------------------------------------------------

    planner = Planner(

        llm=llm,

        state=state,

        tool_registry=registry,

        event_bus=bus,

    )

    # ----------------------------------------------------
    # Executor
    # ----------------------------------------------------

    executor = Executor(

        state=state,

        tool_registry=registry,

        event_bus=bus,
        
        validator=ExecutionValidator(tool_registry=registry)
    )

    # ----------------------------------------------------
    # PLAN
    # ----------------------------------------------------

    planner_output = planner.plan()

    print("=" * 100)
    print("PLANNER OUTPUT")
    print("=" * 100)

    print(planner_output)

    # ----------------------------------------------------
    # EXECUTE
    # ----------------------------------------------------

    result = executor.execute(planner_output)

    print()

    print("=" * 100)
    print("TOOL RESULT")
    print("=" * 100)

    print(result)

    print()

    print("=" * 100)
    print("EXECUTION STATE")
    print("=" * 100)

    print(state.execution)


if __name__ == "__main__":
    main()