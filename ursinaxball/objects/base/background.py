from __future__ import annotations

from enum import Enum

import msgspec
from typing_extensions import Self

from ursinaxball.utils.misc import parse_color_entity, replace_none_values


class BackgroundType(str, Enum):
    Grass = "grass"
    Hockey = "hockey"
    Empty = "none"

    @staticmethod
    def get_background_type(bg_type: str) -> BackgroundType:
        if bg_type == "grass":
            return BackgroundType.Grass
        elif bg_type == "hockey":
            return BackgroundType.Hockey
        else:
            return BackgroundType.Empty


class BackgroundRaw(msgspec.Struct, rename="camel"):
    bg_type: str | None = msgspec.field(default=None, name="type")
    width: float | None = None
    height: float | None = None
    kick_off_radius: float | None = None
    corner_radius: float | None = None
    goal_line: float | None = None
    color: str | None = None

    def apply_default(self) -> Self:
        background_default = BackgroundRaw(
            bg_type="none",
            width=0,
            height=0,
            kick_off_radius=0,
            corner_radius=0,
            goal_line=0,
            color="718C5A",
        )
        replace_none_values(self, background_default)
        return self

    def to_background(self) -> Background:
        background_raw_final = self.apply_default()

        assert background_raw_final.bg_type is not None
        assert background_raw_final.width is not None
        assert background_raw_final.height is not None
        assert background_raw_final.kick_off_radius is not None
        assert background_raw_final.corner_radius is not None
        assert background_raw_final.goal_line is not None
        assert background_raw_final.color is not None

        return Background(
            bg_type=BackgroundType.get_background_type(background_raw_final.bg_type),
            width=background_raw_final.width,
            height=background_raw_final.height,
            kick_off_radius=background_raw_final.kick_off_radius,
            corner_radius=background_raw_final.corner_radius,
            goal_line=background_raw_final.goal_line,
            color=parse_color_entity(background_raw_final.color, False),
        )


class Background(msgspec.Struct, rename="camel"):
    bg_type: BackgroundType
    width: float
    height: float
    kick_off_radius: float
    corner_radius: float
    goal_line: float
    color: tuple[int, int, int, int]
