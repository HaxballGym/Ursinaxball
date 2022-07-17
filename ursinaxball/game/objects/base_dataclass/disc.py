from attr import define, field
import numpy as np
from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.parser import (
    converter_array,
    converter_array_none,
)


@define
class Disc:
    """
    A class to represent the state of a vertex from the game.
    """

    position: np.ndarray = field(converter=converter_array)
    velocity: np.ndarray | None = field(converter=converter_array_none)
    gravity: np.ndarray | None = field(conventer=converter_array_none)
    radius: float | None = None
    inverse_mass: float | None = None
    damping: float | None = None
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None
    bouncing_coefficient: float | None = None
    color: str | None = None
    trait: str | None = None

    def __post_init__(self):
        self.position = np.array(self.position, dtype=float)


if __name__ == "__main__":
    import json
    from cattr import structure

    json_disc = """{
        "position": [
            -370,
            170
        ],
        "trait": "goalNet"
    }"""
    d = structure(json.loads(json_disc), Disc)
    print(d)
