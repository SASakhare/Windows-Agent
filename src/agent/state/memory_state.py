from dataclasses import dataclass, field


@dataclass
class WorkingMemory:
    pass


@dataclass
class SemanticMemory:
    pass


@dataclass
class EpisodicMemory:
    pass


@dataclass
class ProceduralMemory:
    pass


# @dataclass
# class MemoryState:
#     working_memory: WorkingMemory = field(default_factory=WorkingMemory)
#     semantic_memory: SemanticMemory = field(default_factory=SemanticMemory)
#     episodic_memory: EpisodicMemory = field(default_factory=EpisodicMemory)
#     procedural_memory: ProceduralMemory = field(default_factory=ProceduralMemory)



@dataclass
class MemoryState:

    working_memory: dict = field(default_factory=dict)

    semantic_memory: dict = field(default_factory=dict)

    episodic_memory: dict = field(default_factory=dict)

    procedural_memory: dict = field(default_factory=dict)


