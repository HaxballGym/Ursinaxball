from __future__ import annotations

import msgspec


class Trait(msgspec.Struct):
    vis: bool | None = None
    b_coef: float | None = None
    radius: float | None = None
    inv_mass: float | None = None
    speed: tuple[float, float] | None = None
    gravity: tuple[float, float] | None = None
    damping: float | None = None
    c_group: list[str] | None = None
    c_mask: list[str] | None = None
    acceleration: float | None = None
    color: str | tuple[int, int, int] | None = None
    bias: float | None = None
    curve: float | None = None
    curve_f: float | None = None


def get_traits(traits: list | dict) -> dict[str, Trait]:
    if isinstance(traits, list):
        if len(traits) == 0:
            return {}
        else:
            raise ValueError("Invalid property format")
    elif isinstance(traits, dict):
        traits = {trait: msgspec.convert(data, Trait) for trait, data in traits.items()}
    else:
        raise ValueError("Invalid property format")

    return traits
