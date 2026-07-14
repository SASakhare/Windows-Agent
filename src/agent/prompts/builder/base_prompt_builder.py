from abc import ABC, abstractmethod


class BasePromptBuilder(ABC):

    @abstractmethod
    def build(self, state) -> str:
        pass