from dataclasses import dataclass


@dataclass
class LLMConfig:
    '''
    Configuration for LLM Model.
    '''

    provider:str

    model_name:str

    temperature:float = 0.2

    max_tokens:int=2048

    api_key:str|None=None

    base_url:str | None = None
    



























