from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ursinaxball import Game


class Bot(ABC):
    def __init__(self):
        pass

    @staticmethod
    def symmetry_action(action: list[int]) -> list[int]:
        return [-action[0], action[1], action[2]]

    @abstractmethod
    def step(self, game: Game) -> list[int]:
        raise NotImplementedError
