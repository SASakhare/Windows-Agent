from pydantic import ValidationError

from src.agent.reasoner.reasoner_output import ReasonerOutput


class ReasonerValidator:
    """
    Validates the structured output produced by the Reasoner.

    Ensures the LLM response conforms to the ReasonerOutput schema.
    """

    def validate(
        self,
        data: dict,
    ) -> ReasonerOutput:

        try:
            return ReasonerOutput.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"Invalid Reasoner output:\n{exc}"
            ) from exc