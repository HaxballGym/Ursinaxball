from __future__ import annotations

import importlib.resources as pkg_resources
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import msgspec
import numpy as np

from ursinaxball import stadiums
from ursinaxball.objects.base import (
    Background,
    BackgroundRaw,
    Ball,
    CurvedSegment,
    Disc,
    DiscRaw,
    Goal,
    GoalRaw,
    Plane,
    PlaneRaw,
    PlayerDisc,
    PlayerPhysics,
    PlayerPhysicsRaw,
    SegmentRaw,
    StraightSegment,
    Trait,
    Vertex,
    VertexRaw,
    get_ball,
)
from ursinaxball.utils.enums import BaseMap
from ursinaxball.utils.misc import replace_none_values

if TYPE_CHECKING:
    import numpy.typing as npt
    from typing_extensions import Self


class CameraFollow(str, Enum):
    Player = "player"
    Ball = "ball"


class KickOffReset(str, Enum):
    Partial = "partial"
    Full = "full"


class StadiumRaw(msgspec.Struct, rename="camel"):
    name: str
    bg: BackgroundRaw
    width: float | None = None
    height: float | None = None
    camera_width: float | None = None
    camera_height: float | None = None
    max_view_width: float | None = None
    camera_follow: str | None = None
    spawn_distance: float | None = None
    can_be_stored: bool | None = None
    kick_off_reset: str | None = None
    traits: dict[str, Trait] | list | None = None
    vertexes: list[VertexRaw] | None = None
    segments: list[SegmentRaw] | None = None
    goals: list[GoalRaw] | None = None
    discs: list[DiscRaw] | None = None
    planes: list[PlaneRaw] | None = None
    red_spawn_points: list[list[float]] | None = None
    blue_spawn_points: list[list[float]] | None = None
    player_physics: PlayerPhysicsRaw | None = None
    ball_physics: str | dict | None = None

    def apply_default(self) -> Self:
        stadium_default = StadiumRaw(
            name="",
            bg=BackgroundRaw(),
            width=0,
            height=0,
            camera_width=0,
            camera_height=0,
            max_view_width=0,
            camera_follow="ball",
            spawn_distance=200,
            can_be_stored=True,
            kick_off_reset="partial",
            traits={},
            vertexes=[],
            segments=[],
            goals=[],
            discs=[],
            planes=[],
            red_spawn_points=[],
            blue_spawn_points=[],
            player_physics=PlayerPhysicsRaw(),
            ball_physics=None,
        )
        replace_none_values(self, stadium_default)
        return self

    def to_stadium(self) -> Stadium:
        stadium_raw_final = self.apply_default()

        assert stadium_raw_final.width is not None
        assert stadium_raw_final.height is not None
        assert stadium_raw_final.camera_width is not None
        assert stadium_raw_final.camera_height is not None
        assert stadium_raw_final.max_view_width is not None
        assert stadium_raw_final.camera_follow is not None
        assert stadium_raw_final.spawn_distance is not None
        assert stadium_raw_final.can_be_stored is not None
        assert stadium_raw_final.kick_off_reset is not None
        assert stadium_raw_final.traits is not None
        assert stadium_raw_final.vertexes is not None
        assert stadium_raw_final.segments is not None
        assert stadium_raw_final.goals is not None
        assert stadium_raw_final.discs is not None
        assert stadium_raw_final.planes is not None
        assert stadium_raw_final.red_spawn_points is not None
        assert stadium_raw_final.blue_spawn_points is not None
        assert stadium_raw_final.player_physics is not None

        traits = (
            stadium_raw_final.traits
            if isinstance(stadium_raw_final.traits, dict)
            else {}
        )
        stad_discs = [disc.to_disc(traits) for disc in stadium_raw_final.discs]
        ball_physics = get_ball(self.ball_physics, stad_discs, traits)
        discs = [ball_physics, *stad_discs]

        return Stadium(
            name=stadium_raw_final.name,
            bg=stadium_raw_final.bg.to_background(),
            width=stadium_raw_final.width,
            height=stadium_raw_final.height,
            camera_width=stadium_raw_final.camera_width,
            camera_height=stadium_raw_final.camera_height,
            max_view_width=stadium_raw_final.max_view_width,
            camera_follow=CameraFollow(stadium_raw_final.camera_follow),
            spawn_distance=stadium_raw_final.spawn_distance,
            can_be_stored=stadium_raw_final.can_be_stored,
            kick_off_reset=KickOffReset(stadium_raw_final.kick_off_reset),
            traits=traits,
            vertexes=[v.to_vertex(traits) for v in stadium_raw_final.vertexes],
            segments=[seg.to_segment(traits) for seg in stadium_raw_final.segments],
            goals=[goal.to_goal() for goal in stadium_raw_final.goals],
            discs=discs,  # type: ignore
            planes=[plane.to_plane(traits) for plane in stadium_raw_final.planes],
            red_spawn_points=[np.array(p) for p in stadium_raw_final.red_spawn_points],
            blue_spawn_points=[
                np.array(p) for p in stadium_raw_final.blue_spawn_points
            ],
            player_physics=stadium_raw_final.player_physics.to_player_physics(),
            ball_physics=ball_physics,
        )


class Stadium(msgspec.Struct, rename="camel"):
    name: str
    bg: Background
    width: float
    height: float
    camera_width: float
    camera_height: float
    max_view_width: float
    camera_follow: CameraFollow
    spawn_distance: float
    can_be_stored: bool
    kick_off_reset: KickOffReset
    traits: dict[str, Trait]
    vertexes: list[Vertex]
    segments: list[CurvedSegment | StraightSegment]
    goals: list[Goal]
    discs: list[Disc | PlayerDisc]
    planes: list[Plane]
    red_spawn_points: list[npt.NDArray]
    blue_spawn_points: list[npt.NDArray]
    player_physics: PlayerPhysics
    ball_physics: Ball


def load_stadium_external(stadium_map: Path):
    with Path.open(stadium_map, "r") as f:
        data = f.read()

    stadium_raw = msgspec.json.decode(data, type=StadiumRaw)
    return stadium_raw.to_stadium()


def load_stadium_base(stadium_map: BaseMap):
    stadium_file = stadium_map.value
    with pkg_resources.open_text(stadiums, stadium_file) as f:
        data = f.read()

    stadium_raw = msgspec.json.decode(data, type=StadiumRaw)
    return stadium_raw.to_stadium()


def load_stadium(stadium_map: BaseMap | Path):
    if isinstance(stadium_map, BaseMap):
        return load_stadium_base(stadium_map)

    if stadium_map.suffix not in [".json5", ".hbs"]:
        raise ValueError("File name must end with .json5 or .hbs.")
    else:
        return load_stadium_external(stadium_map)
