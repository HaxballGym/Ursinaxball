from __future__ import annotations

import importlib.resources as pkg_resources
import json
from typing import List

from ursinaxball import stadiums
from ursinaxball.common_values import BaseMap
from ursinaxball.objects.base import (
    Background,
    BallPhysics,
    Disc,
    Goal,
    Plane,
    PlayerPhysics,
    Segment,
    Trait,
    Vertex,
)


class Stadium:
    """
    A class to represent the state of a stadium from the game.
    """

    def __init__(self, data: dict):
        self.name: str = data.get("name")
        self.spawn_distance: float = data.get("spawnDistance")
        self.kickoff_reset: str = data.get("kickoffReset", "partial")
        self.camera_follow: str = data.get("cameraFollow")
        self.width: float = data.get("width")
        self.height: float = data.get("height")
        self.kickoff_radius: float = data.get("kickoffRadius")
        self.red_spawn_points: list[list[float]] = data.get("redSpawnPoints", [])
        self.blue_spawn_points: list[list[float]] = data.get("blueSpawnPoints", [])

        traits: dict = data.get("traits")
        traits_name = [t for t in traits]
        traits_data = [traits.get(t) for t in traits_name]
        self.traits: List[Trait] = [
            Trait(v, name) for v, name in zip(traits_data, traits_name)
        ]

        self.background: Background = Background(data.get("bg"))
        self.vertices: List[Vertex] = [Vertex(v, data) for v in data.get("vertexes")]
        self.segments: List[Segment] = [Segment(s, data) for s in data.get("segments")]
        self.goals: List[Goal] = [Goal(g, data) for g in data.get("goals")]
        self.discs: List[Disc] = [Disc(d, data) for d in data.get("discs")]
        self.planes: List[Plane] = [Plane(p, data) for p in data.get("planes")]

        self.player_physics: PlayerPhysics = PlayerPhysics(
            data.get("playerPhysics"), data
        )
        self.ball_physics: BallPhysics = BallPhysics(data.get("ballPhysics"), data)

        self.discs.insert(0, self.ball_physics)

        self.get_y_symmetry()

    def get_y_symmetry(self):
        for point in self.red_spawn_points:
            point[1] *= -1
        for point in self.blue_spawn_points:
            point[1] *= -1


def load_stadium_hbs_str(file_name: str):
    with open(file_name) as f:
        data = json.load(f)
    return Stadium(data)


def load_stadium_hbs_base(file_name: BaseMap):
    stadium_file = file_name.value
    with pkg_resources.open_text(stadiums, stadium_file) as f:
        data = json.load(f)
    return Stadium(data)


def load_stadium_hbs(file_name: BaseMap | str):
    """
    Load a stadium from a file with extension hbs.
    """
    if not file_name.endswith(".hbs"):
        raise ValueError("File name must end with .hbs")

    if isinstance(file_name, BaseMap):
        return load_stadium_hbs_base(file_name)
    else:
        return load_stadium_hbs_str(file_name)


if __name__ == "__main__":
    haxball_map = BaseMap.CLASSIC
    stadium = load_stadium_hbs(haxball_map)
    print(stadium.name)
