from attr import define, field

from ursinaxball.game.common_values import CollisionFlag
from ursinaxball.game.objects.base_dataclass.vertex import Vertex


@define
class Segment:
    """
    A class to represent the state of a vertex from the game.
    """

    vertices_index: list[int]
    vertices: list[Vertex] = field(init=False)
    collision_group: CollisionFlag | None = None
    collision_mask: CollisionFlag | None = None

    bouncing_coefficient: float | None = None
    curve: float | None = None
    curveF: float | None = None
    bias: float | None = None
    visible: bool | None = None
    color: str | None = None
    trait: str | None = None


if __name__ == "__main__":
    import json

    from cattr import structure

    json_segment = """{
        "position": [
            -370,
            170
        ],
        "trait": "goalNet"
    }"""
    s = structure(json.loads(json_segment), Segment)
    print(s)
