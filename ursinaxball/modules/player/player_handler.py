from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

import numpy as np

from ursinaxball.common_values import (
    ActionBin,
    CollisionFlag,
    TeamColor,
    TeamID,
)
from ursinaxball.modules import GameScore
from ursinaxball.modules.bots import Bot
from ursinaxball.modules.player import PlayerData
from ursinaxball.objects import Stadium
from ursinaxball.objects.base import PlayerPhysics

if TYPE_CHECKING:
    from ursinaxball import Game


class PlayerHandler(object):
    id_iterate = itertools.count()

    def __init__(
        self, name: str, team: int = TeamID.SPECTATOR, bot: Bot | None = None
    ) -> None:
        self.id = next(PlayerHandler.id_iterate)
        self.name = name
        self.team = team
        self.bot = bot
        self.action: list[int] = []
        self.kicking = False
        # kick_cancel is used to make sure you stop kicking after hitting the ball
        self._kick_cancel = False
        self.disc: PlayerPhysics = PlayerPhysics()
        self.player_data = PlayerData()

    def set_color(self) -> None:
        if self.team == TeamID.RED:
            self.disc.color = TeamColor.RED
        elif self.team == TeamID.BLUE:
            self.disc.color = TeamColor.BLUE

    def is_kicking(self) -> bool:
        return self.kicking and not self._kick_cancel

    def step(self, game: Game) -> list[int] | None:
        if self.bot is not None:
            return self.bot.step(self, game)
        return None

    def resolve_movement(self, stadium_game: Stadium, game_score: GameScore) -> None:
        if self.disc is not None:
            self.kicking = self.action[ActionBin.KICK] == 1
            if self.action[ActionBin.KICK] == 0:
                self._kick_cancel = False

        player_has_kicked = False
        for disc_stadium in stadium_game.discs:
            if (
                disc_stadium.collision_group & CollisionFlag.KICK
            ) != 0 and disc_stadium != self.disc:
                dist = np.linalg.norm(disc_stadium.position - self.disc.position)
                if (dist - self.disc.radius - disc_stadium.radius) < 4:
                    if self.is_kicking():
                        normal = (disc_stadium.position - self.disc.position) / dist
                        disc_stadium.velocity += normal * self.disc.kick_strength
                        self.disc.velocity += (
                            normal * -self.disc.kickback * self.disc.inverse_mass
                        )
                        player_has_kicked = True
                        self.player_data.update_touch(stadium_game, game_score)
                    else:
                        self.player_data.update_touch(stadium_game, game_score)

        if player_has_kicked:
            self._kick_cancel = True

        input_direction = (
            self.action[:2] / np.linalg.norm(self.action[:2])
            if np.linalg.norm(self.action[:2]) > 0
            else np.array([0.0, 0.0])
        )
        player_acceleration = (
            self.disc.kicking_acceleration
            if self.is_kicking()
            else self.disc.acceleration
        )
        self.disc.velocity += input_direction * player_acceleration
