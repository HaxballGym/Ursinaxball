import numpy as np
from attr import define, field

from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.parser import converter_array


@define
class Disc:
    """
    A class to represent the state of a vertex from the game.
    """

    position: np.ndarray = field(converter=converter_array)
    velocity: np.ndarray | None = field(default=None, converter=converter_array)
    gravity: np.ndarray | None = field(default=None, converter=converter_array)
    radius: float | None = None
    inverse_mass: float | None = None
    damping: float | None = None
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None
    bouncing_coefficient: float | None = None
    color: str | None = None
    trait: str | None = None


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
