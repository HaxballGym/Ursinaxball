import numpy as np
from attr import define, field

from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.parser import converter_array


@define
class Vertex:
    """
    A class to represent the state of a vertex from the game.
    """

    position: np.ndarray = field(converter=converter_array)
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None
    bouncing_coefficient: float | None = None
    trait: str | None = None


if __name__ == "__main__":
    import json

    from cattr import structure

    json_vertex = """{
        "position": [
            -370,
            170
        ],
        "trait": "goalNet"
    }"""
    v = structure(json.loads(json_vertex), Vertex)
    print(v)
