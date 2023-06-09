from __future__ import annotations

import numpy as np

from ursinaxball.common_values import CollisionFlag
from ursinaxball.objects.base import PhysicsObject


class Vertex(PhysicsObject):
    """
    A class to represent the state of a vertex from the game.
    """

    def __init__(self, data_object: dict | None, data_stadium: dict):
        if data_object is None:
            data_object = {}

        self.collision_group: int = self.transform_collision_dict(
            data_object.get("cGroup")
        )
        self.collision_mask: int = self.transform_collision_dict(
            data_object.get("cMask")
        )
        self.position: np.ndarray = np.array(
            [data_object.get("x"), data_object.get("y")], dtype=float
        )
        self.bouncing_coefficient: float = data_object.get("bCoef")
        self.trait = data_object.get("trait")

        self.apply_trait(self, data_stadium)
        self.apply_default_values()
        self.get_y_symmetry()

    def apply_default_values(self):
        """
        Applies the default values to the vertex if they are none
        """
        if self.collision_group is None:
            self.collision_group = CollisionFlag.WALL
        if self.collision_mask is None:
            self.collision_mask = CollisionFlag.ALL
        if self.bouncing_coefficient is None:
            self.bouncing_coefficient = 1

    def get_y_symmetry(self):
        self.position[1] *= -1
