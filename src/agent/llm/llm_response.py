from dataclasses import dataclass
from typing import Any



@dataclass
class LLMResponse:
    '''
    Standard response returned by LLM Providers.
    '''


    content:str

    model:str=""

    usage:dict[str,Any]|None=None

    raw_response:Any=None











































