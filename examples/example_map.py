from dataclasses import dataclass

import numpy as np
from ursina.input_handler import Keys, held_keys

from ursinaxball import Game
from ursinaxball.modules import GameScore, PlayerHandler
from ursinaxball.utils.enums import BaseMap, TeamID

game = Game(
    enable_vsync=True,
    stadium_file=BaseMap.OBSTACLE_WINKY,
)
game.score = GameScore(time_limit=0, score_limit=0)
player_physics = game.stadium_store.player_physics

player_red = PlayerHandler("P1", player_physics, TeamID.RED)
game.add_players([player_red])


@dataclass
class InputPlayer:
    left: list[str] | list[Keys]
    right: list[str] | list[Keys]
    up: list[str] | list[Keys]
    down: list[str] | list[Keys]
    shoot: list[str] | list[Keys]


input_player = InputPlayer(
    left=[Keys.left_arrow],
    right=[Keys.right_arrow],
    up=[Keys.up_arrow],
    down=[Keys.down_arrow],
    shoot=["x"],
)


def action_handle(actions_player_output: list[int], inputs_player: InputPlayer):
    actions_player_output = [0, 0, 0]
    for key, value in held_keys.items():
        if value != 0:
            if key in inputs_player.left:
                actions_player_output[0] -= 1
            if key in inputs_player.right:
                actions_player_output[0] += 1
            if key in inputs_player.up:
                actions_player_output[1] += 1
            if key in inputs_player.down:
                actions_player_output[1] -= 1
            if key in inputs_player.shoot:
                actions_player_output[2] += 1
    return actions_player_output


while True:
    save_rec = False
    game.reset(save_recording=save_rec)
    done = False
    actions = [[0, 0, 0]]
    while not done:
        actions[0] = action_handle(actions[0], input_player)
        done = game.step(np.array(actions))
