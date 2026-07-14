from src.agent.events.event_bus import EventBus
from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory
from src.agent.messages.messages import Message, MessageRole
from src.agent.planner.planner import Planner
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry

from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.windows.file_manager import FileManagerTool
from src.agent.tools.windows.network import NetworkTool

tool_registry = ToolRegistry()

tool_registry.register(BrowserTool)
tool_registry.register(FileManagerTool)
tool_registry.register(NetworkTool)


state = AgentState()

state.goal.user_goal = "Open google.com"

state.conversation.conversation_history = [
    Message(MessageRole.USER, content="Open google.com")
]

config = LLMConfig(
    provider="ollama",
    model_name="qwen3:14b",
)

llm = LLMFactory.create(config)


bus = EventBus()


planner = Planner(
    llm=llm,
    state=state,
    tool_registry=tool_registry,
    event_bus=bus,
)


result = planner.plan()


# with open("planner_plan.txt",'w',encoding='utf-8') as file:
#     file.write(result) # type: ignore

print(result)
