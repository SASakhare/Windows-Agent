from typing import Type
from pydantic import BaseModel
from langchain_core.language_models import BaseChatModel
from src.agent.llm.base_llm import BaseLLM
from src.agent.llm.llm_response import LLMResponse


class LangChainLLM(BaseLLM):
    """
    LangChain based LLM Wrapper
    """

    def __init__(
        self,
        model: BaseChatModel,
    ) -> None:
        super().__init__()

        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate normal text response
        """
        response = self.model.invoke(prompt)

        return LLMResponse(
            content=response.content,  # type: ignore
            raw_response=response,
        )

    def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """
        Generate structured response.

        Langchain validate output
        against provided schema.
        """

        structured_model = self.model.with_structured_output(schema)

        result=structured_model.invoke(prompt)

        return result # type: ignore
