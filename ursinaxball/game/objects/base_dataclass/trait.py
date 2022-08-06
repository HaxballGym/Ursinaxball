from attrs import define, field
import numpy as np

from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.parser import (
    converter_array,
    converter_array_none,
)


@define
class Trait:
    name: str
    visible: bool | None = None
    bouncing_coefficient: float | None = None
    radius: float | None = None
    inverse_mass: float | None = None
    damping: float | None = None
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None
    color: str | None = None
    velocity: np.ndarray | None = field(default=None, converter=converter_array_none)
    gravity: np.ndarray | None = field(default=None, converter=converter_array_none)


if __name__ == "__main__":
    import json
    from cattr import structure

    json_trait = """{
        "bouncing_coefficient": 0.5,
        "collision_mask": 6,
        "visible": false,
        "name": "kickOffBarrier"
    }"""
    t = structure(json.loads(json_trait), Trait)
    print(t)
