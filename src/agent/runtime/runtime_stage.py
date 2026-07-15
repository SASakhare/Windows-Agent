from __future__ import annotations

from abc import ABC, abstractmethod

from src.agent.runtime.runtime_context import RuntimeContext


class RuntimeStage(ABC):
    """
    Base class for every runtime stage.

    A stage performs exactly one responsibility and
    updates the RuntimeContext.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def execute(
        self,
        context: RuntimeContext,
    ) -> None:
        ...