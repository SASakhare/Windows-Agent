from abc import ABC,abstractmethod 
from typing import Any



class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self)->str:  # type: ignore
        pass

    @property
    @abstractmethod
    def description(self)->str:  # type: ignore
        pass


    @abstractmethod
    def execute(self,action:str,**kwargs)->Any:
        pass





















