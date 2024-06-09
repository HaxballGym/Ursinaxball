from __future__ import annotations

from math import pi
from typing import TYPE_CHECKING

import msgspec
import numpy as np
import numpy.typing as npt
from ursina import Entity, Pipe
from ursina.color import rgb

from ursinaxball.utils.enums import CollisionFlag
from ursinaxball.utils.misc import parse_color_entity, replace_none_values
from ursinaxball.utils.rendering import arc

if TYPE_CHECKING:
    from typing_extensions import Self

    from ursinaxball.objects.base.trait import Trait
    from ursinaxball.objects.base.vertex import Vertex


class SegmentRaw(msgspec.Struct, rename="camel"):
    v0: int
    v1: int
    b_coef: float | None = None
    curve: float | None = None
    curve_f: float | None = None
    bias: float | None = None
    c_group: list[str] | None = None
    c_mask: list[str] | None = None
    vis: bool | None = None
    color: str | tuple[int, int, int] | None = None
    trait: str | None = None

    def apply_trait(self, traits: dict[str, Trait]) -> Self:
        if self.trait is None:
            return self
        trait = traits.get(self.trait)
        if trait is None:
            return self

        segment_trait = SegmentRaw(
            v0=-1,
            v1=-1,
            b_coef=trait.b_coef,
            curve=trait.curve,
            curve_f=trait.curve_f,
            bias=trait.bias,
            c_group=trait.c_group,
            c_mask=trait.c_mask,
            vis=trait.vis,
            color=trait.color,
        )

        replace_none_values(self, segment_trait)
        return self

    def apply_default(self) -> Self:
        segment_default = SegmentRaw(
            v0=-1,
            v1=-1,
            b_coef=1,
            curve=0,
            curve_f=0,
            bias=0,
            c_group=["wall"],
            c_mask=["all"],
            vis=True,
            color="000000",
        )
        replace_none_values(self, segment_default)
        return self

    def to_segment(self, traits: dict[str, Trait]) -> CurvedSegment | StraightSegment:
        segment_raw_final = self.apply_trait(traits).apply_default()

        assert segment_raw_final.v0 >= 0
        assert segment_raw_final.v1 >= 0
        assert segment_raw_final.b_coef is not None
        assert segment_raw_final.curve is not None
        assert segment_raw_final.curve_f is not None
        assert segment_raw_final.bias is not None
        assert segment_raw_final.c_group is not None
        assert segment_raw_final.c_mask is not None
        assert segment_raw_final.vis is not None
        assert segment_raw_final.color is not None

        kwargs = {
            "vertex_indices": (segment_raw_final.v0, segment_raw_final.v1),
            "b_coef": segment_raw_final.b_coef,
            "bias": segment_raw_final.bias,
            "c_group": CollisionFlag.from_list(segment_raw_final.c_group),
            "c_mask": CollisionFlag.from_list(segment_raw_final.c_mask),
            "vis": segment_raw_final.vis,
            "color": parse_color_entity(segment_raw_final.color, False),
        }

        if self.curve != 0 or self.curve_f != 0:
            curved_segment = CurvedSegment(**kwargs).get_curve(
                segment_raw_final.curve, segment_raw_final.curve_f
            )
            return curved_segment

        return StraightSegment(**kwargs)


class StraightSegment(msgspec.Struct, rename="camel"):
    vertex_indices: tuple[int, int]
    b_coef: float
    bias: float
    c_group: CollisionFlag
    c_mask: CollisionFlag
    vis: bool
    color: tuple[int, int, int, int]

    def get_entity(self, vertexes: list[Vertex]) -> Entity | None:
        if self.vis is False:
            return None

        vert_mesh = tuple(
            (vertexes[v].position[0], vertexes[v].position[1], 0)
            for v in self.vertex_indices
        )
        line_entity_mesh = Entity(
            model=Pipe(
                path=vert_mesh,
                thicknesses=[3],
            ),
            color=rgb(*self.color),
        )

        return line_entity_mesh


class CurvedSegment(StraightSegment, rename="camel"):
    curve: float = msgspec.field(default=0)

    def get_curve(self, curve: float, curve_f: float) -> Self:
        if curve_f != 0:
            self.curve = curve_f
            return self

        curve_final = curve
        if curve_final < 0:
            curve_final *= -1
            self.bias *= -1
            self.vertex_indices = (self.vertex_indices[1], self.vertex_indices[0])

        curve_final *= np.pi / 180
        lim_inf = 10 * np.pi / 180
        lim_sup = 170 * np.pi / 180
        if lim_inf < curve_final < lim_sup:
            curve_final = 1 / np.tan(curve_final / 2)

        self.curve = curve_final
        return self

    def circle_center(
        self,
        v0_pos: npt.NDArray[np.float64],
        v1_pos: npt.NDArray[np.float64],
        curve: float,
    ) -> npt.NDArray[np.float64]:
        vec_center = (v1_pos - v0_pos) / 2
        circle_center_x: float = v0_pos[0] + vec_center[0] - vec_center[1] * curve
        circle_center_y: float = v0_pos[1] + vec_center[1] + vec_center[0] * curve
        return np.array([circle_center_x, circle_center_y])

    def circle_radius(
        self,
        v0_pos: npt.NDArray[np.float64],
        v1_pos: npt.NDArray[np.float64],
        curve: float,
    ) -> float:
        center = self.circle_center(v0_pos, v1_pos, curve)
        return float(np.linalg.norm(center - v0_pos))

    def circle_tangeants(
        self,
        v0_pos: npt.NDArray[np.float64],
        v1_pos: npt.NDArray[np.float64],
        curve: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        center = self.circle_center(v0_pos, v1_pos, curve)
        return v1_pos - center, v0_pos - center

    def circle_angles(
        self,
        v0_pos: npt.NDArray[np.float64],
        v1_pos: npt.NDArray[np.float64],
        curve: float,
    ) -> tuple[float, float]:
        center = self.circle_center(v0_pos, v1_pos, curve)
        angle_0 = np.arctan2(v0_pos[1] - center[1], v0_pos[0] - center[0])
        angle_1 = np.arctan2(v1_pos[1] - center[1], v1_pos[0] - center[0])
        while angle_1 < angle_0:
            angle_1 += 2 * np.pi
        return angle_0, angle_1

    def get_entity(self, vertexes: list[Vertex]) -> Entity | None:
        if self.vis is False:
            return None

        args_fn = (
            vertexes[self.vertex_indices[0]].position,
            vertexes[self.vertex_indices[1]].position,
            self.curve,
        )
        circle_center = self.circle_center(*args_fn)
        circle_angles = self.circle_angles(*args_fn)
        circle_radius = self.circle_radius(*args_fn)

        nb_segments = int((circle_angles[1] - circle_angles[0]) / (2 * pi) * 64)

        arc_vertices = arc(
            x=circle_center[0],
            y=circle_center[1],
            radius=circle_radius,
            start_angle=circle_angles[0],
            end_angle=circle_angles[1],
            segments=nb_segments,
            clockwise=True,
        )
        vert_mesh = tuple((v[0], v[1], 0) for (_, v) in enumerate(arc_vertices))

        line_entity_mesh = Entity(
            model=Pipe(
                path=vert_mesh,
                thicknesses=[3],
            ),
            color=rgb(*self.color),
        )

        return line_entity_mesh


Segment = CurvedSegment | StraightSegment
