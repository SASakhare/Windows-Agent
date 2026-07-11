from dataclasses import dataclass, field


@dataclass
class WorldState:

    data: dict = field(default_factory=dict)
