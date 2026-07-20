from dataclasses import dataclass, field


@dataclass
class ReasonerState:

    objective: str = ""

    strategy: str = ""

    current_focus: str = ""

    understanding: str = ""
    
    planner_guidance: str = ""

    assumptions: list[str] = field(default_factory=list)

    constraints: list[str] = field(default_factory=list)

    lessons: list[str] = field(default_factory=list)

    known_failures: list[str] = field(default_factory=list)

    confidence: float = 0.0



