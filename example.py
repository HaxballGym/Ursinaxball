from dataclasses import dataclass
import random

from ursina import Keys, held_keys

from ursinaxball import Game
from ursinaxball.common_values import BaseMap, TeamID
from ursinaxball.modules import GameScore, PlayerHandler

game = Game(
    folder_rec="./recordings/",
    enable_vsync=False,
    stadium_file=BaseMap.CLASSIC,
)
team_size = 1
tick_skip = 15


game.score = GameScore(time_limit=3, score_limit=3)

players_red = [PlayerHandler(f"P{i}", TeamID.RED) for i in range(team_size)]
players_blue = [
    PlayerHandler(f"P{team_size + i}", TeamID.BLUE) for i in range(team_size)
]
players = players_red + players_blue

game.add_players(players)


@dataclass
class InputPlayer:
    left: list[str]
    right: list[str]
    up: list[str]
    down: list[str]
    shoot: list[str]


input_player = InputPlayer(
    left=[Keys.left_arrow],
    right=[Keys.right_arrow],
    up=[Keys.up_arrow],
    down=[Keys.down_arrow],
    shoot=["l"],
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


def action_sample():
    RA = random.randint(-1, 1)
    UA = random.randint(-1, 1)
    SA = random.randint(0, 1)
    return [RA, UA, SA]


while True:
    save_rec = False
    game.reset(save_recording=save_rec)
    steps = 0
    done = False
    actions = [[0, 0, 0], [0, 0, 0]]
    while not done:
        actions[0] = action_handle(actions[0], input_player)
        if steps % (tick_skip + 1) == 0:
            actions[1] = action_sample()
        done = game.step(actions)
        steps += 1
