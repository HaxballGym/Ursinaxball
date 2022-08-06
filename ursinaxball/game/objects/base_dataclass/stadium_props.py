import numpy as np
from attrs import Factory, define, field

from ursinaxball.game.objects.base_dataclass.parser import converter_array


@define
class StadiumProps:
    name: str
    width: float
    height: float
    spawn_distance: float
    camera_width: float = field(
        default=Factory(lambda self: self.width, takes_self=True)
    )
    camera_height: float = field(
        default=Factory(lambda self: self.height, takes_self=True)
    )
    max_view_width: float = 0
    camera_follow: str = "ball"
    can_be_stored: bool = True
    kickoff_reset: str = "partial"
    red_spawn_points: np.ndarray = field(factory=list, converter=converter_array)
    blue_spawn_points: np.ndarray = field(factory=list, converter=converter_array)


if __name__ == "__main__":
    import json

    from cattr import structure

    json_stadium_props = """{
        "name": "Classic",
        "width": 420,
        "height": 200,
        "spawn_distance": 277.5
    }"""
    sp = structure(json.loads(json_stadium_props), StadiumProps)
    print(sp)
