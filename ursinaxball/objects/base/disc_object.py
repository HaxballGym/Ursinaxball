from __future__ import annotations

import copy

import numpy as np
from ursina import Entity

from ursinaxball.common_values import CollisionFlag
from ursinaxball.objects.base import PhysicsObject


class Disc(PhysicsObject):
    """
    A class to represent the state of a disc from the game.
    """

    def __init__(
        self, data_object: dict | None = None, data_stadium: dict | None = None
    ):
        if data_object is None:
            data_object = {}

        self.collision_group: int = self.transform_collision_dict(
            data_object.get("cGroup")
        )
        self.collision_mask: int = self.transform_collision_dict(
            data_object.get("cMask")
        )
        self.position: np.ndarray = np.array(data_object.get("pos"), dtype=float)
        self.velocity: np.ndarray = np.array(data_object.get("speed"), dtype=float)
        self.gravity: np.ndarray = np.array(data_object.get("gravity"), dtype=float)
        self.bouncing_coefficient: float = data_object.get("bCoef")
        self.radius: float = data_object.get("radius")
        self.inverse_mass: float = data_object.get("invMass")
        self.damping: float = data_object.get("damping")
        self.color: str = data_object.get("color")
        self.trait = data_object.get("trait")

        self.apply_trait(self, data_stadium)
        self.apply_default_values()
        self.get_y_symmetry()

    def apply_default_values(self):
        if self.collision_group is None:
            self.collision_group = CollisionFlag.ALL
        if self.collision_mask is None:
            self.collision_mask = CollisionFlag.ALL
        if len(self.velocity.shape) == 0:
            self.velocity = np.zeros(2)
        if len(self.gravity.shape) == 0:
            self.gravity = np.zeros(2)
        if self.bouncing_coefficient is None:
            self.bouncing_coefficient = 0.5
        if self.radius is None:
            self.radius = 10
        if self.inverse_mass is None:
            self.inverse_mass = 1
        if self.damping is None:
            self.damping = 0.99
        if self.color is None:
            self.color = "FFFFFF"

    def copy(self, other: "Disc") -> None:
        self.collision_group = copy.copy(other.collision_group)
        self.collision_mask = copy.copy(other.collision_mask)
        self.position = copy.copy(other.position)
        self.velocity = copy.copy(other.velocity)
        self.gravity = copy.copy(other.gravity)
        self.bouncing_coefficient = copy.copy(other.bouncing_coefficient)
        self.radius = copy.copy(other.radius)
        self.inverse_mass = copy.copy(other.inverse_mass)
        self.damping = copy.copy(other.damping)
        self.color = copy.copy(other.color)

    def get_y_symmetry(self):
        if len(self.position.shape) > 0:
            self.position[1] *= -1
        if len(self.velocity.shape) > 0:
            self.velocity[1] *= -1
        if len(self.gravity.shape) > 0:
            self.gravity[1] *= -1

    def get_entity(self) -> Entity:
        disc_parent = Entity(
            x=self.position[0],
            y=self.position[1],
            z=0,
            always_on_top=True,
        )

        Entity(
            parent=disc_parent,
            model="circle",
            color=self.parse_color_entity("000000"),
            scale=(self.radius + 0.75) * 2,
        )

        Entity(
            parent=disc_parent,
            model="circle",
            color=self.parse_color_entity(self.color),
            scale=(self.radius - 0.75) * 2,
        )

        return disc_parent
