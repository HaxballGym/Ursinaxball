from ursinaxball.utils.enums import CollisionFlag

GRASS_BORDER_COLOR = "C7E6BD"
HOCKEY_BORDER_COLOR = "E9CC6E"
DEFAULT_BORDER_COLOR = "000000"

GRASS_FILL_COLOR = "718C5A"
HOCKEY_FILL_COLOR = "555555"
DEFAULT_FILL_COLOR = "000000"


DICT_COLLISION = {
    "": CollisionFlag.NONE,
    "ball": CollisionFlag.BALL,
    "red": CollisionFlag.RED,
    "blue": CollisionFlag.BLUE,
    "redKO": CollisionFlag.REDKO,
    "blueKO": CollisionFlag.BLUEKO,
    "wall": CollisionFlag.WALL,
    "all": CollisionFlag.ALL,
    "kick": CollisionFlag.KICK,
    "score": CollisionFlag.SCORE,
    "c0": CollisionFlag.C0,
    "c1": CollisionFlag.C1,
    "c2": CollisionFlag.C2,
    "c3": CollisionFlag.C3,
}
