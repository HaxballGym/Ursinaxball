import random
import time

from ursina import Keys, held_keys

from ursinaxball import Game
from ursinaxball.common_values import TeamID, BaseMap
from ursinaxball.modules import GameScore, PlayerHandler

game = Game(
    folder_rec="./recordings/",
    enable_vsync=False,
    stadium_file=BaseMap.PENALTY,
)
team_size = 1
tick_skip = 15
tick_limit = 1 * 60 * 60


game.score = GameScore(time_limit=1, score_limit=1)

players_red = [PlayerHandler(f"P{i}", TeamID.RED) for i in range(team_size)]
players_blue = [
    PlayerHandler(f"P{team_size + i}", TeamID.BLUE) for i in range(team_size)
]
players = players_red + players_blue

game.add_players(players)

actions_player = [0, 0, 0]


def action_sample():
    RA = random.randint(-1, 1)
    UA = random.randint(-1, 1)
    SA = random.randint(0, 1)
    return [RA, UA, SA]


def action_handle():
    global actions_player
    actions_player = [0, 0, 0]
    for key, value in held_keys.items():
        if value != 0:
            if key == Keys.right_arrow:
                actions_player[0] += 1
            if key == Keys.left_arrow:
                actions_player[0] -= 1
            if key == Keys.up_arrow:
                actions_player[1] += 1
            if key == Keys.down_arrow:
                actions_player[1] -= 1
            if key == "x":
                actions_player[2] += 1


while True:
    save_rec = False
    game.reset(save_recording=save_rec)
    done = False
    steps = 0
    t0 = time.time()
    frame_time = time.time()
    actions = [actions_player, [0, 0, 0]]
    while not done and steps < tick_limit:
        current_time = time.time()
        if current_time - frame_time >= 0:
            time.sleep(current_time - frame_time)

        frame_time = time.time()
        action_handle()
        actions[0] = actions_player
        if steps % (tick_skip + 1) == 0:
            # actions[0] = action_sample()
            actions[1] = action_sample()
        done = game.step(actions)
        steps += 1

    length = time.time() - t0
    print("Step time: {:1.5f} | Episode time: {:.2f}".format(length / steps, length))
