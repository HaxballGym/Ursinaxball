from __future__ import annotations

import copy

import numpy as np

from ursinaxball.common_values import CollisionFlag
from ursinaxball.objects.base import Disc


class PlayerPhysics(Disc):
    """
    A class to represent the player disc object from the game.
    """

    def __init__(self, data_object: dict | None = None, data_stadium=None):
        if data_object is None:
            data_object = {}

        self.player_id = -1
        self.acceleration: float = data_object.get("acceleration")
        self.kicking_acceleration: float = data_object.get("kickingAcceleration")
        self.kicking_damping: float = data_object.get("kickingDamping")
        self.kick_strength: float = data_object.get("kickStrength")
        self.kickback: float = data_object.get("kickback")

        super().__init__(data_object, data_stadium)

        self.position = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.color = "FFFFFF"
        del self.trait

    def apply_default_values(self):
        """
        Applies the default values to the player if they are none
        """
        if self.bouncing_coefficient is None:
            self.bouncing_coefficient = 0.5
        if self.collision_group is None:
            self.collision_group = CollisionFlag.NONE
        if self.collision_mask is None:
            self.collision_mask = CollisionFlag.ALL
        if len(self.gravity.shape) == 0:
            self.gravity = np.zeros(2)
        if self.radius is None:
            self.radius = 15
        if self.inverse_mass is None:
            self.inverse_mass = 0.5
        if self.damping is None:
            self.damping = 0.96
        if self.acceleration is None:
            self.acceleration = 0.1
        if self.kicking_acceleration is None:
            self.kicking_acceleration = 0.07
        if self.kicking_damping is None:
            self.kicking_damping = 0.96
        if self.kick_strength is None:
            self.kick_strength = 5
        if self.kickback is None:
            self.kickback = 0

    def copy(self, other: "PlayerPhysics") -> None:
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
        self.acceleration = copy.copy(other.acceleration)
        self.kicking_acceleration: float = copy.copy(other.kicking_acceleration)
        self.kicking_damping: float = copy.copy(other.kicking_damping)
        self.kick_strength: float = copy.copy(other.kick_strength)
        self.kickback: float = copy.copy(other.kickback)
