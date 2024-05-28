from __future__ import annotations

from typing import TYPE_CHECKING

import msgspec
import numpy as np
import numpy.typing as npt

from ursinaxball.utils.enums import CollisionFlag
from ursinaxball.utils.misc import parse_color_entity, replace_none_values

if TYPE_CHECKING:
    from typing import Self

    from ursinaxball.objects.base.trait import Trait


class DiscRaw(msgspec.Struct, rename="camel"):
    pos: tuple[float, float]
    speed: tuple[float, float] | None = None
    gravity: tuple[float, float] | None = None
    radius: float | None = None
    inv_mass: float | None = None
    damping: float | None = None
    b_coef: float | None = None
    color: str | tuple[int, int, int] | None = None
    c_group: list[str] | None = None
    c_mask: list[str] | None = None
    trait: str | None = None

    def apply_trait(self, traits: dict[str, Trait]) -> Self:
        if self.trait is None:
            return self
        trait = traits.get(self.trait)
        if trait is None:
            return self

        disc_trait = DiscRaw(
            pos=(0.0, 0.0),
            speed=trait.speed,
            gravity=trait.gravity,
            radius=trait.radius,
            inv_mass=trait.inv_mass,
            damping=trait.damping,
            b_coef=trait.b_coef,
            color=trait.color,
            c_group=trait.c_group,
            c_mask=trait.c_mask,
        )
        replace_none_values(self, disc_trait)
        return self

    def apply_default(self) -> Self:
        disc_default = DiscRaw(
            pos=(0.0, 0.0),
            speed=(0.0, 0.0),
            gravity=(0.0, 0.0),
            radius=10,
            inv_mass=1,
            damping=0.99,
            b_coef=0.5,
            color="FFFFFF",
            c_group=["all"],
            c_mask=["all"],
        )
        replace_none_values(self, disc_default)
        return self

    def to_disc(self, traits: dict[str, Trait]) -> Disc:
        disc_raw_final = self.apply_trait(traits).apply_default()

        assert disc_raw_final.speed is not None
        assert disc_raw_final.gravity is not None
        assert disc_raw_final.radius is not None
        assert disc_raw_final.inv_mass is not None
        assert disc_raw_final.damping is not None
        assert disc_raw_final.b_coef is not None
        assert disc_raw_final.color is not None
        assert disc_raw_final.c_group is not None
        assert disc_raw_final.c_mask is not None

        return Disc(
            position=np.array(disc_raw_final.pos),
            speed=np.array(disc_raw_final.speed),
            gravity=np.array(disc_raw_final.gravity),
            radius=disc_raw_final.radius,
            inv_mass=disc_raw_final.inv_mass,
            damping=disc_raw_final.damping,
            b_coef=disc_raw_final.b_coef,
            color=parse_color_entity(disc_raw_final.color, True),
            c_group=CollisionFlag.from_list(disc_raw_final.c_group),
            c_mask=CollisionFlag.from_list(disc_raw_final.c_mask),
        )


class Disc(msgspec.Struct, rename="camel"):
    position: npt.NDArray[np.float64]
    speed: npt.NDArray[np.float64]
    gravity: npt.NDArray[np.float64]
    radius: float
    inv_mass: float
    damping: float
    b_coef: float
    color: tuple[int, int, int, int]
    c_group: CollisionFlag
    c_mask: CollisionFlag
