from __future__ import annotations

import time

from src.agent.events.event import Event
from src.agent.events.event_bus import EventBus
from src.agent.events.event_types import EventTypes


from src.agent.executor.config import ExecutorConfig
from src.agent.executor.validator import ExecutionValidator
from src.agent.planner.planner_output import PlannerOutput

from src.agent.state.agent_state import AgentState
from src.agent.state.execution_state import ExecutionStatus


from src.agent.tools.registry import ToolRegistry
from src.agent.tools.tool_result import ToolResult

from src.agent.executor.exceptions import ExecutorError



class Executor:

    """
    Executes actions produced by the Planner.

    Responsibilities
    ----------------
    1. Receive PlannerOutput.
    2. Execute the selected tool action.
    3. Update ExecutionState.
    4. Publish execution events.
    5. Return ToolResult.

    The Executor NEVER decides what to execute.
    It only performs the action selected by the Planner.
    """

    def __init__(
        self,
        state:AgentState,
        tool_registry:ToolRegistry,
        event_bus:EventBus,
        validator:ExecutionValidator,
        config:ExecutorConfig | None= None
        ) -> None:
        

        self._state=state
        self._tool_registry=tool_registry
        self._event_bus=event_bus
        self._validator=validator
        self._config=config or ExecutorConfig()


    
    def execute(
        self,
        planner_output:PlannerOutput,
        ) ->ToolResult:
        

        action=planner_output.action

        execution=self._state.execution

        execution.active_tool=action.tool
        execution.active_action=action.action
        execution.execution_status=ExecutionStatus.RUNNING
        execution.error=None

        if self._config.publish_events:
            self._event_bus.publish(
                Event(
                    EventTypes.ACTION_STARTED,
                    "executor",
                    {
                        "tool":action.tool,
                        "action":action.action,
                    }
                )
            )


        start=time.perf_counter()


        try:
            if self._config.validate_before_execution :
                self._validator.validate(planner_output)

            result=self._tool_registry.execute(
                tool_name=action.tool,
                action=action.action,
                **action.arguments,
            )

            execution.tool_result=result

            if result.success:
                execution.execution_status=ExecutionStatus.SUCCESS
            else:
                execution.execution_status=ExecutionStatus.FAILED
                execution.error=result.error

            execution.execution_time=(
                time.perf_counter()-start
            )
            if self._config.publish_events:

                self._event_bus.publish(
                    Event(
                        EventTypes.ACTION_EXECUTED,
                        "executor",
                        {
                            "tool":action.tool,
                            "action":action.action,
                            "result":result,
                        }
                    )
                )

            return result
        
        except ExecutorError:

            raise

        except Exception as exc:
            

            execution.execution_status=ExecutionStatus.FAILED
            execution.error=str(exc)

            execution.execution_time=(
                time.perf_counter()-start
            )

            if self._config.publish_events:
            
                self._event_bus.publish(
                    Event(
                        EventTypes.ACTION_FAILED,
                        "executor",
                        {
                            "tool":action.tool,
                            "action":action.action,
                            "error":str(exc),
                        }
                    )
                )


            return ToolResult(
                success=False,
                error=str(exc),
                tool="",
                action="",
                result=None,
            )



































