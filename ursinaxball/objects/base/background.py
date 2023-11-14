from __future__ import annotations

from enum import Enum

import msgspec


class BackgroundType(str, Enum):
    grass = "grass"
    hockey = "hockey"
    other = "other"


class BackgroundRaw(msgspec.Struct, rename="camel"):
    bg_type: str | None = msgspec.field(default=None, name="type")
    width: float | None = None
    height: float | None = None
    kick_off_radius: float | None = None
    corner_radius: float | None = None
    goal_line: float | None = None
    color: str | None = None


class Background(msgspec.Struct, rename="camel"):
    bg_type: BackgroundType
    width: float
    height: float
    kick_off_radius: float
    corner_radius: float
    goal_line: float
    color: tuple[int, int, int, int]
