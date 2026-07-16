from src.agent.prompts.formatter.base_formatter import BaseFormatter
from src.agent.state.metadata_state import MetadataState


class MetadataFormatter(BaseFormatter):

    def format(   # type: ignore
        self,
        state: MetadataState,
    ) -> str:

        result = []

        result.append("=" * 60)
        result.append("METADATA")
        result.append("=" * 60)

        result.append("")

        result.append(
            f"Task ID : {state.task_id or 'None'}"
        )

        result.append(
            f"Agent Status : {state.agent_status.value}"
        )

        result.append(
            f"Started At : {state.started_at or 'None'}"
        )

        result.append(
            f"Updated At : {state.updated_at or 'None'}"
        )

        return "\n".join(result)