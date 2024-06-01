import numpy as np

from ursinaxball.game import Game, GameScore
from ursinaxball.modules import PlayerHandler
from ursinaxball.modules.bots import ConstantActionBot
from ursinaxball.utils.enums import TeamID


def test_game():
    game = Game(enable_renderer=False, enable_recorder=False)
    player_physics = game.stadium_store.player_physics

    custom_score = GameScore(time_limit=1, score_limit=1)
    game.score = custom_score

    bot_1 = ConstantActionBot([1, 0, 0])
    bot_2 = ConstantActionBot([1, 1, 1], symmetry=True)

    player_red = PlayerHandler("P0", TeamID.RED, bot=bot_1)
    player_blue = PlayerHandler("P1", TeamID.BLUE, bot=bot_2)
    game.add_players([player_red, player_blue])

    game.start()

    done = False
    while not done:
        actions_player_1 = player_red.step(game)
        actions_player_2 = player_blue.step(game)
        done = game.step(np.array([actions_player_1, actions_player_2]))

    assert game.score.ticks == 176
