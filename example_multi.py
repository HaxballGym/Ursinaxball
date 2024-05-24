from dataclasses import dataclass

import numpy as np
from ursina.input_handler import Keys, held_keys

from ursinaxball import Game
from ursinaxball.common_values import BaseMap, TeamID
from ursinaxball.modules import GameScore, PlayerHandler

game = Game(
    folder_rec="./recordings/",
    enable_vsync=True,
    stadium_file=BaseMap.CLASSIC,
)
team_size = 1


game.score = GameScore(time_limit=3, score_limit=3)

players_red = [PlayerHandler(f"P{i}", TeamID.RED) for i in range(team_size)]
players_blue = [
    PlayerHandler(f"P{team_size + i}", TeamID.BLUE) for i in range(team_size)
]
players = players_red + players_blue

game.add_players(players)


@dataclass
class InputPlayer:
    left: list[str] | list[Keys]
    right: list[str] | list[Keys]
    up: list[str] | list[Keys]
    down: list[str] | list[Keys]
    shoot: list[str] | list[Keys]


input_player_1 = InputPlayer(
    left=[Keys.left_arrow],
    right=[Keys.right_arrow],
    up=[Keys.up_arrow],
    down=[Keys.down_arrow],
    shoot=["l"],
)

input_player_2 = InputPlayer(
    left=["a"],
    right=["d"],
    up=["w"],
    down=["s"],
    shoot=["b"],
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
    actions = [[0, 0, 0], [0, 0, 0]]
    while not done:
        actions[0] = action_handle(actions[0], input_player_1)
        actions[1] = action_handle(actions[1], input_player_2)
        done = game.step(np.array(actions))
