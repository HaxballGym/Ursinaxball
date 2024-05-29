from __future__ import annotations

from typing import TypeVar

import msgspec
from ursina import Color

T = TypeVar("T", bound=msgspec.Struct)


def replace_none_values(self: T, other: T) -> None:
    for key, _ in self.__rich_repr__():
        if getattr(self, key) is None:
            setattr(self, key, getattr(other, key))


def parse_color_entity(
    color: str | tuple[int, int, int], transparent_supported: bool
) -> tuple[int, int, int, int]:
    if color == "transparent":
        if transparent_supported:
            return (0, 0, 0, 0)
        else:
            raise ValueError("transparent is not supported")

    if isinstance(color, tuple):
        if len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            return (*color, 255)
        else:
            raise ValueError("color is not a tuple of 3 integers between 0 and 255")
    elif isinstance(color, str):
        (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        return (r, g, b, 255)
    else:
        raise ValueError("color is not a tuple or a string")


def parse_color_entity_ursina(
    color: str | tuple[int, int, int], transparent_supported: bool
) -> Color:
    color_tuple = parse_color_entity(color, transparent_supported)
    return Color(*color_tuple)
