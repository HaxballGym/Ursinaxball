from __future__ import annotations

from abc import ABC, abstractmethod

from numpy import cos, sin
from ursina.color import Color, rgba

from ursinaxball.common_values import DICT_COLLISION, DICT_KEYS


class PhysicsObject(ABC):
    """Base class for all physics objects in the game."""

    trait: str | None = None

    @abstractmethod
    def __init__(self, data_object: dict | None, data_stadium: dict):
        pass

    @staticmethod
    def apply_trait(self, data: dict) -> None:
        """
        Applies the trait to the physics object.

        Args:
            data: Dictionary containing traits data
        """
        if not data or not data.get("traits") or not self.trait:
            return

        trait_value = data["traits"].get(self.trait, {})
        for key, value in trait_value.items():
            key_object = DICT_KEYS.get(key)
            if (
                not key_object
                or not hasattr(self, key_object)
                or getattr(self, key_object) is not None
            ):
                continue

            final_value = (
                self.transform_collision_dict(value)
                if key_object in ("collision_group", "collision_mask")
                else value
            )
            setattr(self, key_object, final_value)

    @abstractmethod
    def apply_default_values(self):
        """
        Applies the default values to the physics object if they are none
        """

    @staticmethod
    def transform_collision_dict(collision_dict: dict) -> int:
        """
        Transforms the collision into a float.
        For example, ["ball", "red", "blue", "wall"] should return 1 + 2 + 4 + 32 = 39
        """
        if collision_dict is None:
            return None
        else:
            return sum(DICT_COLLISION[key] for key in collision_dict)

    @staticmethod
    def parse_color_entity(color: str) -> Color:
        if color == "transparent":
            return rgba(0, 0, 0, 0)

        (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        return rgba(r, g, b)

    @staticmethod
    def arc(
        x: float,
        y: float,
        radius: float,
        start_angle: float,
        end_angle: float,
        clockwise: bool = True,
        segments: int = 16,
    ) -> list:
        """
        Returns a list of points for an arc.
        """
        points = []
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * i / segments
            x_pos = x + radius * cos(angle)
            y_pos = y + radius * sin(angle)
            points.append((x_pos, y_pos))
        if clockwise:
            return points[::-1]
        else:
            return points
