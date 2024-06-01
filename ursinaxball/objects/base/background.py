from __future__ import annotations

from enum import Enum
from math import pi

import msgspec
from typing_extensions import Self
from ursina import Color, Entity, Mesh, Pipe, Sky

from ursinaxball.utils.misc import parse_color_entity, replace_none_values
from ursinaxball.utils.rendering import arc


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


BACKGROUND_COLORS = {
    "grass": (113, 140, 90, 255),
    "hockey": (113, 140, 90, 255),
    "none": (0, 0, 0, 0),
}


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

    def get_limit_entity(self) -> Entity | None:
        if self.bg_type not in [BackgroundType.Grass, BackgroundType.Hockey]:
            return None

        if self.width is not None and self.height is not None:
            vertices_entity = (
                (-self.width - 1.25, -self.height, 0),
                (self.width + 1.25, -self.height, 0),
                (self.width, -self.height, 0),
                (self.width, self.height, 0),
                (self.width + 1.25, self.height, 0),
                (-self.width - 1.25, self.height, 0),
                (-self.width, self.height, 0),
                (-self.width, -self.height, 0),
            )

            limit_entity = Entity(
                model=Mesh(
                    vertices=vertices_entity,
                    mode="line",
                    thickness=6,
                ),
                z=0.1,
                color=Color(*self.color),
            )
            return limit_entity

    def get_kickoff_circle_entity(self) -> Entity | None:
        if self.bg_type in [BackgroundType.Grass, BackgroundType.Hockey]:
            circle_vertices = arc(
                x=0,
                y=0,
                radius=self.kick_off_radius,
                start_angle=0,
                end_angle=2 * pi,
                segments=64,
                clockwise=True,
            )
            vert_mesh = tuple((v[0], v[1], 0.1) for v in circle_vertices)

            kickoff_circle_entity = Entity(
                model=Pipe(
                    path=vert_mesh,
                    thicknesses=[3],
                ),
                z=0.1,
                color=Color(*self.color),
            )

            return kickoff_circle_entity

    def get_kickoff_line_entity(self) -> Entity | None:
        if self.bg_type not in [BackgroundType.Grass, BackgroundType.Hockey]:
            return None

        if self.height is not None:
            vertices_entity = (
                (0, -self.height, 0),
                (0, self.height, 0),
            )

            limit_entity = Entity(
                model=Mesh(
                    vertices=vertices_entity,
                    mode="line",
                    thickness=6,
                ),
                z=0.1,
                color=Color(*self.color),
            )
            return limit_entity

    def get_fill_canvas(self) -> Entity:
        color = (
            self.color if self.color is not None else BACKGROUND_COLORS[self.bg_type]
        )
        sky = Sky()
        sky = Entity(
            scale=9900,
            model="quad",
            color=color,
            z=2,
        )
        return sky

    def get_entities(self):
        return [
            self.get_limit_entity(),
            self.get_kickoff_circle_entity(),
            self.get_kickoff_line_entity(),
            self.get_fill_canvas(),
        ]
