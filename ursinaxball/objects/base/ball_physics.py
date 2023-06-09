from __future__ import annotations

import numpy as np

from ursinaxball.common_values import CollisionFlag
from ursinaxball.objects.base import Disc


class BallPhysics(Disc):
    """
    A class to represent the state of a ball from the game.
    """

    def __init__(self, data_object: dict | None, data_stadium: dict):
        if data_object is None:
            data_object = {}

        super().__init__(data_object, data_stadium)

        self.position = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)

        self.collision_group = (
            self.collision_group | CollisionFlag.SCORE | CollisionFlag.KICK
        )
        self.collision_mask = (
            self.collision_mask ^ CollisionFlag.REDKO ^ CollisionFlag.BLUEKO
        )
        del self.trait

    def apply_default_values(self):
        """
        Applies the default values to the ball if they are none
        """
        if self.bouncing_coefficient is None:
            self.bouncing_coefficient = 0.5
        if self.collision_group is None:
            self.collision_group = CollisionFlag.BALL
        if self.collision_mask is None:
            self.collision_mask = CollisionFlag.ALL
        if len(self.gravity.shape) == 0:
            self.gravity = np.zeros(2)
        if self.radius is None:
            self.radius = 10
        if self.inverse_mass is None:
            self.inverse_mass = 1
        if self.damping is None:
            self.damping = 0.99
        if self.color is None:
            self.color = "FFFFFF"
