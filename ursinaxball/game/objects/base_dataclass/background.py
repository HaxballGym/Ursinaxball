from enum import Enum

from attr import define


class BackgroundType(str, Enum):
    GRASS = "grass"
    HOCKEY = "hockey"
    NONE = "none"


@define
class Background:
    """
    A class to represent the state of a background from the game.
    """

    type: BackgroundType | None = None
    width: float | None = None
    height: float | None = None
    kickoff_radius: float | None = None
    corner_radius: float | None = None
    goal_line: float | None = None
    color: str | None = None


if __name__ == "__main__":
    import json

    from cattr import structure

    json_bg = """{
        "type": "grass",
        "width": 370,
        "height": 170,
        "kickoff_radius": 75,
        "corner_radius": 0
    }"""

    bg = structure(json.loads(json_bg), Background)
    print(bg)
