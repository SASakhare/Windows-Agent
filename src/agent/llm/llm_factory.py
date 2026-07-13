from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.langchain_llm import LangChainLLM


class LLMFactory:
    """
    Creates LLM instances based on configuration.
    """

    @staticmethod
    def create(config: LLMConfig):

        if config.provider == "ollama":

            from langchain_ollama import ChatOllama

            model = ChatOllama(
                model=config.model_name,
                temperature=config.temperature,
            )
        
        else:
            raise ValueError(
                f'Unsupported provider :{config.provider}'
            )


        return LangChainLLM(model)