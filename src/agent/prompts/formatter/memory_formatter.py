from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.memory_state import MemoryState


class MemoryFormatter(BaseFormatter):

    def format(   # type: ignore
        self,
        state: MemoryState,
    ) -> str:

        result = []

        result.append("=" * 60)
        result.append("MEMORY")
        result.append("=" * 60)

        result.append("")

        result.append("Working Memory")
        result.append("----------------")
        result.append(
            str(state.working_memory or "Empty")
        )

        result.append("")

        result.append("Semantic Memory")
        result.append("----------------")
        result.append(
            str(state.semantic_memory or "Empty")
        )

        result.append("")

        result.append("Episodic Memory")
        result.append("----------------")
        result.append(
            str(state.episodic_memory or "Empty")
        )

        result.append("")

        result.append("Procedural Memory")
        result.append("----------------")
        result.append(
            str(state.procedural_memory or "Empty")
        )

        return "\n".join(result)