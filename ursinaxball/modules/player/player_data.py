from ursinaxball.modules.systems.game_score import GameScore
from ursinaxball.objects.stadium_object import Stadium


class PlayerData:
    def __init__(self) -> None:
        self.number_touch = 0
        self.number_kick = 0
        self.last_touch_time = 0
        self.last_kick_time = 0

    def update_touch(self, _stadium_game: Stadium, game_score: GameScore):
        self.number_touch += 1
        self.last_touch_time = game_score.time

    def update_kick(self, _stadium_game: Stadium, game_score: GameScore):
        self.number_kick += 1
        self.last_kick_time = game_score.time
