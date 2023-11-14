from __future__ import annotations
from typing import TYPE_CHECKING

import msgspec
import numpy as np
import numpy.typing as npt
from ursinaxball.utils import CollisionFlag, replace_none_values

if TYPE_CHECKING:
    from typing import Self
    from ursinaxball.objects.base.trait import Trait


class PlaneRaw(msgspec.Struct, rename="camel"):
    normal: tuple[float, float]
    dist: float
    b_coef: float | None = None
    c_group: list[str] | None = None
    c_mask: list[str] | None = None
    trait: str | None = None

    def apply_trait(self, traits: dict[str, Trait]) -> Self:
        if self.trait is None:
            return self
        trait = traits.get(self.trait)
        if trait is None:
            return self

        plane_trait = PlaneRaw(
            normal=(0.0, 0.0),
            dist=0.0,
            b_coef=trait.b_coef,
            c_group=trait.c_group,
            c_mask=trait.c_mask,
        )
        replace_none_values(self, plane_trait)
        return self

    def apply_default(self) -> Self:
        plane_default = PlaneRaw(
            normal=(0.0, 0.0),
            dist=0.0,
            b_coef=1,
            c_group=["wall"],
            c_mask=["all"],
        )
        replace_none_values(self, plane_default)
        return self

    def to_plane(self, traits: dict[str, Trait]) -> Plane:
        plane_raw_final = self.apply_trait(traits).apply_default()

        assert plane_raw_final.b_coef is not None
        assert plane_raw_final.c_group is not None
        assert plane_raw_final.c_mask is not None

        return Plane(
            normal=np.array(plane_raw_final.normal),
            dist=plane_raw_final.dist,
            b_coef=plane_raw_final.b_coef,
            c_group=CollisionFlag.from_list(plane_raw_final.c_group),
            c_mask=CollisionFlag.from_list(plane_raw_final.c_mask),
        )


class Plane(msgspec.Struct, rename="camel"):
    normal: npt.NDArray[np.float64]
    dist: float
    b_coef: float
    c_group: CollisionFlag
    c_mask: CollisionFlag
