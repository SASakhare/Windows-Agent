from src.agent.events.event import Event
from src.agent.events.event_bus import EventBus
from src.agent.events.event_types import EventTypes
from src.agent.llm.base_llm import BaseLLM
from src.agent.planner.action_validator import ActionValidator
from src.agent.planner.planner_output import PlannerOutput
from src.agent.planner.planner_prompt import PlannerPrompt
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry


class Planner:
    """
    Responsible for deciding the NEXT action.

    Planner never executes actions.
    Planner never retries actions.
    Planner never verifies actions.

    It only reasons about the next best action.
    """

    def __init__(
        self,
        llm: BaseLLM,
        state: AgentState,
        tool_registry: ToolRegistry,
        event_bus: EventBus,
    ) -> None:

        self._llm = llm

        self._state = state

        self._tool_registry = tool_registry

        self._event_bus = event_bus

        self._prompt_builder = PlannerPrompt()

        self._validator = ActionValidator(tool_registry)

    # ^ =====================================================
    # ^ Public API
    # ^ =====================================================

    def plan(self) -> PlannerOutput:
        """
        Generate the next actions
        """

        prompt = self._build_prompt()
        print("**"*50)
        print("Prompt :")
        print(prompt)
        print("**"*50)
        result = self._call_llm(prompt)

        # self._validate(result)

        self._update_state(result)

        self._publish(result)

        return result

    # ^ =====================================================
    # ^ Internal
    # ^ =====================================================

    def _build_prompt(self) -> str:

        return self._prompt_builder.build(
            self._state,
            self._tool_registry.get_all_schemas(),
        )

    def _call_llm(self, prompt: str) -> PlannerOutput:

        return self._llm.generate_structured(
            prompt,
            PlannerOutput,
        )  # type: ignore

    def _validate(
        self,
        result: PlannerOutput,
    ):

        if result.goal_completed:
            return

        self._validator.validate(result.action)  

    def _update_state(
        self,
        result: PlannerOutput,
    ) -> None:

        planning = self._state.planning

        planning.current_action = result.action

        planning.planner_reasoning = result.thought

        planning.expected_outcome = result.expected_outcome

        planning.goal_completed = result.goal_completed

    def _publish(
        self,
        result: PlannerOutput,
    ) -> None:

        if result.goal_completed:

            self._event_bus.publish(
                Event(
                    event_type=EventTypes.GOAL_COMPLETED,
                    source="Planner",
                    payload=result,
                )
            )

            return

        self._event_bus.publish(
            Event(
                event_type=EventTypes.ACTION_PLANNED,
                source="Planner",
                payload=result.action,
            )
        )
