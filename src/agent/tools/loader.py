
from src.agent.tools.registry import ToolRegistry

from src.agent.tools.browser.browser_tool import BrowserTool
from src.agent.tools.code.code_tool import CodeTool
# from src.agent.tools.reasoning.reasoning_tool import ReasoningTool
from src.agent.tools.speech.speech_tool import SpeechTool
from src.agent.tools.web.search_tool import SearchTool

from src.agent.tools.windows.audio import AudioTool 
from src.agent.tools.windows.clipboard import ClipboardTool
from src.agent.tools.windows.display import DisplayTool 
from src.agent.tools.windows.file_manager import FileManagerTool 
from src.agent.tools.windows.network import NetworkTool 
from src.agent.tools.windows.powertool import PowerTool 
from src.agent.tools.windows.process_manager import ProcessManagerTool 
from src.agent.tools.windows.storage import StorageTool



toolRegister=ToolRegistry()

toolRegister.register(BrowserTool)
toolRegister.register(CodeTool)
# toolRegister.register(ReasoningTool)
toolRegister.register(SpeechTool)
toolRegister.register(SearchTool)
toolRegister.register(AudioTool)
toolRegister.register(ClipboardTool)
toolRegister.register(DisplayTool)
toolRegister.register(FileManagerTool)
toolRegister.register(NetworkTool)
toolRegister.register(PowerTool)
toolRegister.register(ProcessManagerTool)
toolRegister.register(StorageTool)






if __name__=="__main__":
    print("Testing Tool Registry")
    toolRegister=ToolRegistry()
    toolRegister.register(BrowserTool)
    toolRegister.register(SearchTool)
    toolRegister.register(FileManagerTool)

    # print(toolRegister.get_schema(BrowserTool().name))
    print(toolRegister.get_all_schemas())
    result = toolRegister.execute(
        tool_name="file",
        action="create_file",
        file_name="hello.txt"
    )

    print(result)






















