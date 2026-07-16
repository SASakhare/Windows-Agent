from copy import deepcopy
from typing import Any

from src.agent.observer.models.observation import Observation
from src.agent.state.word_state import WorldState


class WorldUpdater:
    """
    Updates the agent's WorldState using the facts extracted
    by the Observer.

    This class is deterministic and contains no LLM logic.
    """

    def update(
        self,
        world: WorldState,
        observation: Observation,
    ) -> WorldState:
        """
        Merge observation.world_updates into the existing world state.
        """

        if not observation.world_updates:
            return world

        self._deep_merge(
            world.data,
            observation.world_updates,
        )

        return world

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _deep_merge(
        self,
        target: dict[str, Any],
        source: dict[str, Any],
    ) -> None:
        """
        Recursively merge source into target.
        """

        for key, value in source.items():

            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_merge(
                    target[key],
                    value,
                )

            else:
                target[key] = deepcopy(value)