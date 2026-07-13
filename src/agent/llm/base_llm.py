from abc import ABC,abstractmethod
from typing import Type


from pydantic import BaseModel

from src.agent.llm.llm_response import LLMResponse



class BaseLLM(ABC):

    '''
    Abstract interface for all LLM Providers
    '''

    @abstractmethod
    def generate(
        self,
        prompt: str,
    )->LLMResponse:
        '''
        Generate normal text response
        '''

        pass



    @abstractmethod
    def generate_structured(
        self,
        prompt:str,
        schema:Type[BaseModel],
    )->BaseModel:
        
        '''
        Generate response following given schema.

        Example:
        
        PlannerOutput
        ReflectionOutput
        RecoveryOutput
        '''

        pass





























