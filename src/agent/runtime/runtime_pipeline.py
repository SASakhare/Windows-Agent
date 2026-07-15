from src.agent.runtime.runtime_stage import RuntimeStage


class RuntimePipeline:

    def __init__(self):

        self._stages: list[RuntimeStage] = []

    def add_stage(
        self,
        stage: RuntimeStage,
    ) -> None:

        self._stages.append(stage)

    @property
    def stages(self):

        return tuple(self._stages)