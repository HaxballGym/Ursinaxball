import numpy as np
from attr import define, field

from ursinaxball.game.common_values import TeamID
from ursinaxball.game.objects.base_dataclass.parser import converter_array


@define
class Goal:
    """
    A class to represent the state of a goal from the game.
    """

    points: np.ndarray = field(converter=converter_array)
    team: TeamID


if __name__ == "__main__":
    import json

    from cattr import structure

    json_goal = """{
      "team": 1,
      "points": [
        [
          -370,
          64
        ],
        [
          -370,
          -64
        ]
      ]
    }"""
    g = structure(json.loads(json_goal), Goal)
    print(g)
