from langchain_core.language_models import BaseChatModel

from src.agent.llm.base_llm import BaseLLM
from src.agent.prompts.builder.reasoner_prompt_builder import ReasonerPromptBuilder
from src.agent.reasoner.reasoner_config import ReasonerConfig
from src.agent.reasoner.reasoner_output import ReasonerOutput
from src.agent.reasoner.reasoner_validator import ReasonerValidator
from src.agent.state.agent_state import AgentState


class Reasoner:
    """
    Strategic reasoning engine.

    The Reasoner analyzes the current AgentState,
    updates the agent's strategic understanding,
    and produces guidance for the Planner.

    It never selects tools or executable actions.
    """

    def __init__(
        self,
        llm: BaseLLM,
        prompt_builder: ReasonerPromptBuilder,
        validator: ReasonerValidator,
        config: ReasonerConfig,
    ) -> None:

        self._llm = llm

        self._prompt_builder = prompt_builder

        self._validator = validator

        self._config = config

    def reason(
        self,
        state: AgentState,
    ) -> ReasonerOutput:
        """
        Executes one strategic reasoning cycle.
        """

        prompt = self._prompt_builder.build(state)

        response = self._llm.generate_structured(prompt,ReasonerOutput)

        result = self._validator.validate(response) # type: ignore

        self._update_state(
            state,
            result,
        )

        return result

    def _update_state(
        self,
        state: AgentState,
        result: ReasonerOutput,
    ) -> None:
        """
        Synchronize the persistent ReasonerState with the latest reasoning.
        """

        reasoner = state.reasoner

        reasoner.objective = result.objective
        reasoner.understanding = result.understanding
        reasoner.strategy = result.strategy
        reasoner.current_focus = result.current_focus
        reasoner.planner_guidance = result.planner_guidance

        reasoner.assumptions = result.assumptions
        reasoner.constraints = result.constraints
        reasoner.lessons = result.lessons
        reasoner.known_failures = result.known_failures

        reasoner.confidence = result.confidence