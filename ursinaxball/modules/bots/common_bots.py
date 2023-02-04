from __future__ import annotations

from typing import TYPE_CHECKING

from ursinaxball.modules.bots import Bot

if TYPE_CHECKING:
    from ursinaxball import Game


class ConstantActionBot(Bot):
    """
    This bot goes presses the same keys every step
    """

    def __init__(self, action: list[int], symmetry: bool = False):
        super().__init__()
        self.action = action
        self.symmetry = symmetry

    def step(self, game: Game) -> list[int]:
        action_final = (
            self.action if not self.symmetry else self.symmetry_action(self.action)
        )
        return action_final
