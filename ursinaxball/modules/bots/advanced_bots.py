from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ursinaxball.common_values import ActionBin, TeamID, GameState
from ursinaxball.modules.bots import Bot
from ursinaxball.objects.base import Disc, Goal


if TYPE_CHECKING:
    from ursinaxball import Game
    from ursinaxball.modules import PlayerHandler


def segment_intersection(
    segment1: list[tuple[float, float]], segment2: list[tuple[float, float]]
) -> list[float] | None:
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    # Calculate the determinant
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # If the determinant is zero, the segments are parallel
    if d == 0:
        return None

    # Calculate the x and y coordinates of the intersection point
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d

    # Check if the intersection point is within the segments
    if (
        (x1 <= x <= x2 or x2 <= x <= x1)
        and (y1 <= y <= y2 or y2 <= y <= y1)
        and (x3 <= x <= x4 or x4 <= x <= x3)
        and (y3 <= y <= y4 or y4 <= y <= y3)
    ):
        return [x, y]
    else:
        return None


def position_keeper(goal: Goal, ball: Disc) -> list[float]:
    center_goal = (
        (goal.points[0][0] + goal.points[1][0]) / 2,
        (goal.points[0][1] + goal.points[1][1]) / 2,
    )

    x_keeper = (abs(center_goal[0]) - 60) * np.sign(center_goal[0])
    default_x = (abs(goal.points[0][0]) - 25) * np.sign(center_goal[0])

    intersection = segment_intersection(
        segment1=[center_goal, tuple(ball.position)],
        segment2=[(x_keeper, goal.points[0][1]), (x_keeper, goal.points[1][1])],
    )
    if intersection is not None:
        return intersection

    intersection = segment_intersection(
        segment1=[center_goal, tuple(ball.position)],
        segment2=[
            (goal.points[0][0], goal.points[0][1]),
            (x_keeper, goal.points[0][1]),
        ],
    )
    if intersection is not None:
        if intersection[0] < default_x and center_goal[0] < 0:
            intersection[0] = default_x
        elif intersection[0] > default_x and center_goal[0] > 0:
            intersection[0] = default_x
        return intersection

    intersection = segment_intersection(
        segment1=[center_goal, tuple(ball.position)],
        segment2=[
            (goal.points[1][0], goal.points[1][1]),
            (x_keeper, goal.points[1][1]),
        ],
    )
    if intersection is not None:
        if intersection[0] < default_x and center_goal[0] < 0:
            intersection[0] = default_x
        elif intersection[0] > default_x and center_goal[0] > 0:
            intersection[0] = default_x
        return intersection

    intersection = segment_intersection(
        segment1=[center_goal, tuple(ball.position)],
        segment2=[
            (goal.points[0][0], goal.points[0][1]),
            (goal.points[1][0], goal.points[1][1]),
        ],
    )

    if intersection is None:
        return list(center_goal)

    return intersection


def follow_point(
    player: PlayerHandler, point: list[float], precision: int
) -> list[int]:
    inputs_player = [0, 0, 0]
    if player.disc.position[0] - point[0] > precision:
        inputs_player[ActionBin.RIGHT] -= 1
    if player.disc.position[0] - point[0] < -precision:
        inputs_player[ActionBin.RIGHT] += 1

    if player.disc.position[1] - point[1] > precision:
        inputs_player[ActionBin.UP] -= 1
    if player.disc.position[1] - point[1] < -precision:
        inputs_player[ActionBin.UP] += 1

    return inputs_player


def shoot_disc_close(
    player: PlayerHandler, disc: Disc, precision: int, previous_actions: list[int]
) -> int:
    dist = np.linalg.norm(disc.position - player.disc.position)
    if (dist - player.disc.radius - disc.radius) < precision:
        if player._kick_cancel and previous_actions[ActionBin.KICK] == 1:
            return 0
        else:
            return 1

    return 0


class GoalkeeperBot(Bot):
    """
    This bot acts as a pure goalkeeper
    """

    def __init__(self, tick_skip: int):
        super().__init__(tick_skip=tick_skip)
        self.previous_actions: list[int] = []

    def step_game_kickoff(self, player: PlayerHandler, game: Game) -> list[int]:
        ball = game.stadium_game.discs[0]
        threshold = 2
        if game.team_kickoff == player.team:
            random_kick = np.random.uniform(-ball.radius / 2, ball.radius / 2)
            point = [ball.position[0], ball.position[1] + random_kick]
            inputs_player = follow_point(player, point, threshold)
            inputs_player[ActionBin.KICK] = shoot_disc_close(
                player, ball, 15, self.previous_actions
            )
            self.previous_actions = inputs_player
        else:
            inputs_player = self.step_game_play(player, game)

        return inputs_player

    def step_game_play(self, player: PlayerHandler, game: Game) -> list[int]:
        ball = game.stadium_game.discs[0]
        threshold = 2
        goal = (
            game.stadium_game.goals[0]
            if player.team == TeamID.RED
            else game.stadium_game.goals[1]
        )
        new_pos = position_keeper(goal, ball)
        inputs_player = follow_point(player, new_pos, threshold)
        inputs_player[ActionBin.KICK] = shoot_disc_close(
            player, ball, 15, self.previous_actions
        )

        self.previous_actions = inputs_player
        return inputs_player

    def step_game(self, player: PlayerHandler, game: Game) -> list[int]:
        if game.state == GameState.KICKOFF:
            return self.step_game_kickoff(player, game)
        elif game.state == GameState.PLAYING:
            return self.step_game_play(player, game)

        return [0, 0, 0]
