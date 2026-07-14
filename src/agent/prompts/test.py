from src.agent.events.event_bus import EventBus

from src.agent.prompts.builder.planner_prompt_builder import PlannerPromptBuilder

from src.agent.prompts.formatter.tool_formatter import ToolFormatter
from src.agent.prompts.formatter.conversation_formatter import ConversationFormatter
from src.agent.prompts.formatter.planning_formatter import PlanningFormatter

from src.agent.prompts.formatter.word_formatter import WorldFormatter
from src.agent.state.agent_state import AgentState
from src.agent.messages.messages import Message,MessageRole
from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.registry import ToolRegistry
from src.agent.tools.windows.file_manager import FileManagerTool
from src.agent.tools.windows.network import NetworkTool




def main():

    state = AgentState()

    state.goal.user_goal = "Open google.com"

    state.conversation.conversation_history.append(
        Message(
            role=MessageRole.USER,
            content="Open google.com",
        )
    )

    registry = ToolRegistry()

    registry.register(BrowserTool)
    registry.register(FileManagerTool)
    registry.register(NetworkTool)

    builder = PlannerPromptBuilder(
        tool_formatter=ToolFormatter(),
        conversation_formatter=ConversationFormatter(),
        planning_formatter=PlanningFormatter(),
        world_formatter=WorldFormatter(),
    )

    prompt = builder.build(
        state=state,
        tool_registry=registry,
    )

    # print("=" * 120)
    # print(prompt)
    # print("=" * 120)

    # * Saving the File :
    with open('prompt_file.txt','w',encoding='utf-8') as file:
        file.write(prompt)
    

    print("Prompt file Saving Completed.")


if __name__ == "__main__":
    main()