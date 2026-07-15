"""
ExecutionState should answer:

    What tool is currently running?
    What action is being executed?
    Did it succeed?
    What was the output?
    Did it fail?
    How many retries have been attempted?

"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


from src.agent.tools.tool_result import ToolResult


class ExecutionStatus(Enum):

    IDLE='idle'
    RUNNING='running'
    SUCCESS='success'
    FAILED='failed'




@dataclass
class ExecutionState:

    active_tool:str="" 

    active_action:str=""

    execution_status:ExecutionStatus=ExecutionStatus.IDLE

    tool_result:Optional[ToolResult]=None

    error:Optional[str]=None

    retry_count:int=0

    execution_time:float=0.0





























