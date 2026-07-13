from src.agent.llm.llm_config import LLMConfig
from src.agent.llm.llm_factory import LLMFactory



config=LLMConfig(
    provider="ollama",
    model_name="qwen3:14b"
)


llm=LLMFactory.create(config)


response=llm.generate(
    "Explain recursion"
)


print(response.content)














