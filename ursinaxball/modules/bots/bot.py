from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ursinaxball import Game
    from ursinaxball.modules import PlayerHandler


class Bot(ABC):
    def __init__(self, symmetry=False, tick_skip=0):
        self.symmetry = symmetry
        self.tick_skip = tick_skip
        self.game_ticks = 0
        pass

    @staticmethod
    def symmetry_action(action: list[int]) -> list[int]:
        return [-action[0], action[1], action[2]]

    @abstractmethod
    def step_game(self, player: PlayerHandler, game: Game) -> list[int]:
        raise NotImplementedError

    def step(self, player: PlayerHandler, game: Game) -> list[int]:
        if self.game_ticks % (self.tick_skip + 1) == 0:
            self.actions = self.step_game(player, game)
            if self.symmetry:
                self.actions = self.symmetry_action(self.actions)
        self.game_ticks += 1
        return self.actions
