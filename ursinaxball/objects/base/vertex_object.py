from __future__ import annotations
from typing import TYPE_CHECKING

import msgspec
import numpy as np
import numpy.typing as npt
from ursinaxball.common_values import CollisionFlag

if TYPE_CHECKING:
    from typing import Self
    from ursinaxball.objects.base.trait_object import Trait


class VertexRaw(msgspec.Struct, rename="camel"):
    x: float
    y: float
    b_coef: float | None = None
    c_group: list[str] | None = None
    c_mask: list[str] | None = None
    trait: str | None = None

    def replace_none_values(self, other: VertexRaw) -> None:
        self.b_coef = self.b_coef if self.b_coef is not None else other.b_coef
        self.c_group = self.c_group if self.c_group is not None else other.c_group
        self.c_mask = self.c_mask if self.c_mask is not None else other.c_mask

    def apply_trait(self, traits: dict[str, Trait]) -> Self:
        if self.trait is None:
            return self
        trait = traits.get(self.trait)
        if trait is None:
            return self

        vertex_trait = VertexRaw(
            x=0.0,
            y=0.0,
            b_coef=trait.b_coef,
            c_group=trait.c_group,
            c_mask=trait.c_mask,
        )
        self.replace_none_values(vertex_trait)
        return self

    def apply_default(self) -> Self:
        vertex_default = VertexRaw(
            x=0.0,
            y=0.0,
            b_coef=1,
            c_group=["wall"],
            c_mask=["all"],
        )
        self.replace_none_values(vertex_default)
        return self

    def to_vertex(self, traits: dict[str, Trait]) -> Vertex:
        vertex_raw_final = self.apply_trait(traits).apply_default()

        assert vertex_raw_final.b_coef is not None
        assert vertex_raw_final.c_group is not None
        assert vertex_raw_final.c_mask is not None

        return Vertex(
            position=np.array([vertex_raw_final.x, vertex_raw_final.y]),
            b_coef=vertex_raw_final.b_coef,
            c_group=CollisionFlag.from_list(vertex_raw_final.c_group),
            c_mask=CollisionFlag.from_list(vertex_raw_final.c_mask),
        )


class Vertex(msgspec.Struct, rename="camel"):
    position: npt.NDArray[np.float64]
    b_coef: float
    c_group: CollisionFlag
    c_mask: CollisionFlag
