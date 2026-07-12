from src.agent.models.action import Action
from src.agent.tools.registry import ToolRegistry


class ActionValidator:

    def validate(
        self,
        action: Action,
        registry: ToolRegistry,
    ) -> bool:
        ...
