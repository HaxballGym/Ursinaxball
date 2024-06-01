from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import msgspec
import numpy as np
import numpy.typing as npt

from ursinaxball.objects.base.disc import Disc
from ursinaxball.utils.enums import CollisionFlag
from ursinaxball.utils.misc import replace_none_values

if TYPE_CHECKING:
    from typing_extensions import Self


class PlayerPhysicsRaw(msgspec.Struct, rename="camel"):
    gravity: list[float] | None = None
    radius: float | None = None
    inv_mass: float | None = None
    damping: float | None = None
    b_coef: float | None = None
    c_group: list[str] | None = None
    acceleration: float | None = None
    kicking_acceleration: float | None = None
    kicking_damping: float | None = None
    kick_strength: float | None = None
    kickback: float | None = None

    def apply_default(self) -> Self:
        player_default = PlayerPhysicsRaw(
            gravity=[0.0, 0.0],
            radius=15,
            inv_mass=1,
            damping=0.96,
            b_coef=0.5,
            c_group=[],
            acceleration=0.1,
            kicking_acceleration=0.07,
            kicking_damping=0.96,
            kick_strength=5,
            kickback=0,
        )
        replace_none_values(self, player_default)
        return self

    def to_player_physics(self) -> PlayerPhysics:
        player_raw_final = self.apply_default()

        assert player_raw_final.gravity is not None
        assert player_raw_final.radius is not None
        assert player_raw_final.inv_mass is not None
        assert player_raw_final.damping is not None
        assert player_raw_final.b_coef is not None
        assert player_raw_final.c_group is not None
        assert player_raw_final.acceleration is not None
        assert player_raw_final.kicking_acceleration is not None
        assert player_raw_final.kicking_damping is not None
        assert player_raw_final.kick_strength is not None
        assert player_raw_final.kickback is not None

        return PlayerPhysics(
            gravity=np.array(player_raw_final.gravity),
            radius=player_raw_final.radius,
            inv_mass=player_raw_final.inv_mass,
            damping=player_raw_final.damping,
            b_coef=player_raw_final.b_coef,
            c_group=CollisionFlag.from_list(player_raw_final.c_group),
            acceleration=player_raw_final.acceleration,
            kicking_acceleration=player_raw_final.kicking_acceleration,
            kicking_damping=player_raw_final.kicking_damping,
            kick_strength=player_raw_final.kick_strength,
            kickback=player_raw_final.kickback,
        )


class PlayerPhysics(msgspec.Struct, rename="camel"):
    gravity: npt.NDArray[np.float64]
    radius: float
    inv_mass: float
    damping: float
    b_coef: float
    c_group: CollisionFlag
    acceleration: float
    kicking_acceleration: float
    kicking_damping: float
    kick_strength: float
    kickback: float


class PlayerDisc(Disc, rename="camel"):
    player_id: int
    acceleration: float
    kicking_acceleration: float
    kicking_damping: float
    kick_strength: float
    kickback: float

    def copy(self, other: PlayerDisc) -> None:
        self.position = copy.copy(other.position)
        self.speed = copy.copy(other.speed)
        self.gravity = copy.copy(other.gravity)
        self.radius = copy.copy(other.radius)
        self.inv_mass = copy.copy(other.inv_mass)
        self.damping = copy.copy(other.damping)
        self.b_coef = copy.copy(other.b_coef)
        self.color = copy.copy(other.color)
        self.c_group = copy.copy(other.c_group)
        self.c_mask = copy.copy(other.c_mask)
        self.acceleration = copy.copy(other.acceleration)
        self.kicking_acceleration = copy.copy(other.kicking_acceleration)
        self.kicking_damping = copy.copy(other.kicking_damping)
        self.kick_strength = copy.copy(other.kick_strength)
        self.kickback = copy.copy(other.kickback)


def get_player_disc(player_id: int, player_physics: PlayerPhysics):
    player_disc = PlayerDisc(
        player_id=player_id,
        position=np.array([0.0, 0.0]),
        speed=np.array([0.0, 0.0]),
        gravity=player_physics.gravity,
        radius=player_physics.radius,
        inv_mass=player_physics.inv_mass,
        damping=player_physics.damping,
        b_coef=player_physics.b_coef,
        color=(255, 255, 255, 255),
        c_group=CollisionFlag.from_list([]),
        c_mask=CollisionFlag.from_list([]),
        acceleration=player_physics.acceleration,
        kicking_acceleration=player_physics.kicking_acceleration,
        kicking_damping=player_physics.kicking_damping,
        kick_strength=player_physics.kick_strength,
        kickback=player_physics.kickback,
    )
    return player_disc
