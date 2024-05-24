from __future__ import annotations

from typing import TYPE_CHECKING
from random import randint

import numpy as np

from ursinaxball.modules.bots import Bot
from ursinaxball.common_values import ActionBin

if TYPE_CHECKING:
    from ursinaxball import Game
    from ursinaxball.modules import PlayerHandler


class ConstantActionBot(Bot):
    """
    This bot presses the same keys every step
    """

    def __init__(self, action: list[int], symmetry: bool = False):
        super().__init__(symmetry=symmetry)
        self.action = action

    def step_game(self, player: PlayerHandler, game: Game) -> list[int]:
        return self.action


class RandomBot(Bot):
    """
    This bot presses random keys every step
    """

    def __init__(self, tick_skip: int):
        super().__init__(tick_skip=tick_skip)

    def step_game(self, player: PlayerHandler, game: Game) -> list[int]:
        RA = randint(-1, 1)
        UA = randint(-1, 1)
        SA = randint(0, 1)
        return [RA, UA, SA]


class ChaseBot(Bot):
    """
    This bot chases the ball and shoots when close enough
    """

    def __init__(self, tick_skip: int):
        super().__init__(tick_skip=tick_skip)
        self.previous_actions = []

    def step_game(self, player: PlayerHandler, game: Game) -> list[int]:
        inputs_player = [0, 0, 0]
        ball = game.stadium_game.discs[0]
        threshold = 2

        if player.disc.position[0] - ball.position[0] > threshold:
            inputs_player[ActionBin.RIGHT] -= 1
        if player.disc.position[0] - ball.position[0] < -threshold:
            inputs_player[ActionBin.RIGHT] += 1

        if player.disc.position[1] - ball.position[1] > threshold:
            inputs_player[ActionBin.UP] -= 1
        if player.disc.position[1] - ball.position[1] < -threshold:
            inputs_player[ActionBin.UP] += 1

        dist = np.linalg.norm(ball.position - player.disc.position)
        if (dist - player.disc.radius - ball.radius) < 15:
            if ~player._kick_cancel and self.previous_actions[ActionBin.KICK] == 1:
                inputs_player[ActionBin.KICK] = 0
            else:
                inputs_player[ActionBin.KICK] = 1

        self.previous_actions = inputs_player
        return inputs_player
