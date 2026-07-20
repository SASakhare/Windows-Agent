from src.agent.events.event import Event
from src.agent.events.event_bus import EventBus
from src.agent.events.event_types import EventTypes
from src.agent.llm.base_llm import BaseLLM
from src.agent.planner.action_validator import ActionValidator
from src.agent.planner.planner_output import PlannerOutput
from src.agent.planner.planner_prompt import PlannerPrompt
from src.agent.prompts.builder.planner_prompt_builder import PlannerPromptBuilder
from src.agent.prompts.formatter.conversation_formatter import ConversationFormatter
from src.agent.prompts.formatter.execution_formatter import ExecutionFormatter
from src.agent.prompts.formatter.planning_formatter import PlanningFormatter
from src.agent.prompts.formatter.recovery_formatter import RecoveryFormatter
from src.agent.prompts.formatter.reflection_formatter import ReflectionFormatter
from src.agent.prompts.formatter.tool_formatter import ToolFormatter
from src.agent.prompts.formatter.word_formatter import WorldFormatter
from src.agent.state.agent_state import AgentState
from src.agent.tools.registry import ToolRegistry
from src.agent.prompts.formatter.reasoner_formatter import ReasonerFormatter


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

        self._prompt_builder = PlannerPromptBuilder(
            reasoner_formatter=ReasonerFormatter(),
            tool_formatter=ToolFormatter(),
            conversation_formatter=ConversationFormatter(),
            planning_formatter=PlanningFormatter(),
            world_formatter=WorldFormatter(),
            execution_formatter=ExecutionFormatter(),
        )

        self._validator = ActionValidator(tool_registry)

    # ^ =====================================================
    # ^ Public API
    # ^ =====================================================

    def plan(self) -> PlannerOutput:
        """
        Generate the next actions
        """

        prompt = self._build_prompt()

        result = self._call_llm(prompt)

        # self._validate(result)
        # with open('prompt_file_from_planner.txt','w',encoding='utf-8') as file:
        #     file.write(prompt)

        # print("Prompt file Saving Completed.")

        self._update_state(result)

        self._publish(result)

        return result

    # ^ =====================================================
    # ^ Internal
    # ^ =====================================================

    def _build_prompt(self) -> str:

        return self._prompt_builder.build(
            state=self._state,
            tool_registry=self._tool_registry,
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
