from abc import ABC, abstractmethod


class BaseFormatter(ABC):

    @abstractmethod
    def format(self, data) -> str:
        """
        Convert an object into an LLM-friendly string.
        """
        raise NotImplementedError
