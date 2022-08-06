import numpy as np
from attrs import define, field

from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.parser import converter_array


@define
class Plane:
    """
    A class to represent the state of a plane from the game.
    """

    normal: np.ndarray = field(converter=converter_array)
    distance_origin: float
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None
    bouncing_coefficient: float | None = None
    trait: str | None = None


if __name__ == "__main__":
    import json

    from cattr import structure

    json_plane = """{
        "distance_origin": -170,
        "normal": [0, 1],
        "trait": "ballArea"
    }"""

    p = structure(json.loads(json_plane), Plane)
    print(p)
