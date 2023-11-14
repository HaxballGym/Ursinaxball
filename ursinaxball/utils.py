from __future__ import annotations

from enum import Enum, IntEnum, IntFlag
from typing import TypeVar

import msgspec

from ursinaxball.constants import DICT_COLLISION

T = TypeVar("T", bound=msgspec.Struct)


def replace_none_values(self: T, other: T) -> None:
    for field in self.__dict__.keys():
        if getattr(self, field) is None:
            setattr(self, field, getattr(other, field))


def parse_color_entity(
    color: str | tuple[int, int, int], transparent_supported: bool
) -> tuple[int, int, int, int]:
    if color == "transparent":
        if transparent_supported:
            return (0, 0, 0, 0)
        else:
            raise ValueError("transparent is not supported")

    if isinstance(color, tuple):
        if len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            return (*color, 255)
        else:
            raise ValueError("color is not a tuple of 3 integers between 0 and 255")
    elif isinstance(color, str):
        (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        return (r, g, b, 255)
    else:
        raise ValueError("color is not a tuple or a string")


class CollisionFlag(IntFlag):
    NONE = 0
    BALL = 1
    RED = 2
    BLUE = 4
    REDKO = 8
    BLUEKO = 16
    WALL = 32
    ALL = 63
    KICK = 64
    SCORE = 128
    C0 = 268435456
    C1 = 536870912
    C2 = 1073741824
    C3 = -2147483648

    @staticmethod
    def from_list(collision_list: list[str]) -> CollisionFlag:
        if collision_list is None:
            raise ValueError("collision_list is None")

        return CollisionFlag(sum([DICT_COLLISION[c] for c in collision_list]))


class TeamID(IntEnum):
    SPECTATOR = 0
    RED = 1
    BLUE = 2


class GameState(IntEnum):
    KICKOFF = 0
    PLAYING = 1
    GOAL = 2
    END = 3


class ActionBin(IntEnum):
    RIGHT = 0
    UP = 1
    KICK = 2


class Input(IntEnum):
    UP = 4
    DOWN = 1
    LEFT = 2
    RIGHT = 8
    SHOOT = 16


class BaseMap(str, Enum):
    CLASSIC = "classic.json5"
    ROUNDED = "rounded.json5"
    BIG = "big.json5"
    FUTSAL_CLASSIC = "futsal-classic.json5"
    FUTSAL_BIG = "futsal-big.json5"
    PENALTY = "penalty-soccer.json5"
    OBSTACLE_WINKY = "obstacle-map-winky.json5"


class TeamColor(str, Enum):
    RED = "E56E56"
    BLUE = "5689E5"
