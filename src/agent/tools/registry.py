from src.agent.tools.base_tool import BaseTool
from src.agent.tools.schema_generator import build_tool_schema


class ToolRegistry:

    def __init__(self) -> None:

        self.__tools = {}
        self.__schemas = {}

    def register(self, tool_class: type[BaseTool]) -> None:

        if not issubclass(tool_class,BaseTool):
            raise TypeError(...)

        instance = tool_class()
        if instance.name in self.__tools:
            raise ValueError(f"Tool '{instance.name}' is already registered.")

        self.__tools[instance.name] = instance
        self.__schemas[instance.name] = build_tool_schema(tool_class)

    def unregister(self, tool_name: str):

        if tool_name not in self.__tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        self.__tools.pop(tool_name)
        self.__schemas.pop(tool_name)

    def get(self, tool_name: str):

        if tool_name not in self.__tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        return self.__tools[tool_name]

    def get_schema(self, tool_name: str):

        if tool_name not in self.__tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        return self.__schemas[tool_name]

    def get_all_schemas(self):

        return self.__schemas.copy()

    def execute(self, tool_name: str, action: str, **kwargs):

        if tool_name not in self.__tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            tool_instance = self.__tools[tool_name]
        except Exception as e:
            raise RuntimeError(
                f"Error executing '{action}' on tool '{tool_name}' :{e}"
            )
        return tool_instance.execute(action, **kwargs)
