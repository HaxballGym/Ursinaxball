from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING

import numpy as np

from ursinaxball.modules import (
    GameActionRecorder,
    GameRenderer,
    GameScore,
    PlayerHandler,
    resolve_collisions,
    update_discs,
)
from ursinaxball.objects.base import Disc, get_player_disc
from ursinaxball.objects.stadium import Stadium, load_stadium
from ursinaxball.utils.constants import PATH_RECORDINGS
from ursinaxball.utils.enums import BaseMap, CollisionFlag, GameState, TeamID

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)


class Game:
    def __init__(
        self,
        stadium_file: BaseMap | Path = BaseMap.CLASSIC,
        folder_rec: Path = PATH_RECORDINGS,
        logging_level: int = logging.DEBUG,
        enable_vsync: bool = True,
        enable_renderer: bool = True,
        fov: int = 550,
        enable_recorder: bool = True,
    ):
        logging.basicConfig(level=logging_level, format="%(levelname)s - %(message)s")

        self.folder_rec = folder_rec
        self.score = GameScore()
        self.state = GameState.KICKOFF
        self.players: list[PlayerHandler] = []
        self.team_kickoff = TeamID.RED
        self.stadium_file = stadium_file
        self.stadium_store: Stadium = load_stadium(self.stadium_file)
        self.stadium_game: Stadium = copy.deepcopy(self.stadium_store)
        self.enable_recorder = enable_recorder
        self.recorder = (
            GameActionRecorder(self, self.folder_rec) if self.enable_recorder else None
        )
        self.enable_renderer = enable_renderer
        self.renderer = (
            GameRenderer(self, enable_vsync, fov) if enable_renderer else None
        )

    def add_player(self, player: PlayerHandler) -> None:
        self.players.append(player)

    def add_players(self, players: list[PlayerHandler]) -> None:
        for player in players:
            self.add_player(player)

    def make_player_action(self, player: PlayerHandler, action: np.ndarray) -> None:
        player.action = action
        player.resolve_movement(self.stadium_game, self.score)

    def get_player_by_id(self, player_id: int) -> PlayerHandler | None:
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    def load_map(self, map_file: Path | BaseMap) -> None:
        """
        Loads a map from a hbs file.
        """
        self.stadium_file = map_file
        self.stadium_store: Stadium = load_stadium(map_file)
        self.stadium_game: Stadium = copy.deepcopy(self.stadium_store)

    def check_goal(self, previous_discs_position: list[Disc]) -> int:
        current_disc_position = [
            disc
            for disc in self.stadium_game.discs
            if disc.c_group & CollisionFlag.SCORE != 0
        ]
        for previous_disc_pos, current_disc_pos in zip(
            previous_discs_position, current_disc_position
        ):
            for goal in self.stadium_game.goals:
                previous_p0 = previous_disc_pos.position - goal.p0
                current_p0 = current_disc_pos.position - goal.p0
                current_p1 = current_disc_pos.position - goal.p1
                disc_vector = current_disc_pos.position - previous_disc_pos.position
                goal_vector = goal.p1 - goal.p0
                if (
                    np.cross(current_p0, disc_vector)
                    * np.cross(current_p1, disc_vector)
                    <= 0
                    and np.cross(previous_p0, goal_vector)
                    * np.cross(current_p0, goal_vector)
                    <= 0
                ):
                    team_score = TeamID.RED if goal.team == "red" else TeamID.BLUE
                    return team_score

        return TeamID.SPECTATOR

    def handle_game_state(self, previous_discs_position: list[Disc]) -> bool:
        self.score.step(self.state)

        if self.state == GameState.KICKOFF:
            for player in self.players:
                if player.disc.position is not None:
                    kickoff_collision = (
                        CollisionFlag.REDKO
                        if self.team_kickoff == TeamID.RED
                        else CollisionFlag.BLUEKO
                    )
                    player.disc.c_mask = CollisionFlag(39 | kickoff_collision)
            ball_disc = self.stadium_game.discs[0]
            if np.linalg.norm(ball_disc.speed) > 0:
                log.debug("Kickoff made")
                self.state = GameState.PLAYING

        elif self.state == GameState.PLAYING:
            for player in self.players:
                if player.disc.position is not None:
                    player.disc.c_mask = CollisionFlag(39)
            team_goal = self.check_goal(previous_discs_position)
            if team_goal != TeamID.SPECTATOR:
                team_goal_string = "Red" if team_goal == TeamID.RED else "Blue"
                log.debug(f"Team {team_goal_string} conceded a goal")
                self.state = GameState.GOAL
                self.score.update_score(team_goal)
                if not self.score.is_game_over():
                    self.team_kickoff = (
                        TeamID.BLUE if team_goal == TeamID.BLUE else TeamID.RED
                    )
            elif self.score.is_game_over():
                self.state = GameState.END
                self.score.end_animation()

        elif self.state == GameState.GOAL:
            self.score.animation_timeout -= 1
            if not self.score.is_animation():
                if self.score.is_game_over():
                    self.state = GameState.END
                    self.score.end_animation()
                else:
                    self.reset_discs_positions()
                    self.state = GameState.KICKOFF

        elif self.state == GameState.END:
            self.score.animation_timeout -= 1
            if not self.score.is_animation():
                return True

        return False

    def reset_discs_positions(self) -> None:
        discs_game = (
            self.stadium_game.discs
            if self.stadium_game.kick_off_reset == "full"
            else [self.stadium_game.discs[0]]
        )
        discs_store = (
            self.stadium_store.discs
            if self.stadium_store.kick_off_reset == "full"
            else [self.stadium_store.discs[0]]
        )

        for disc_game, disc_store in zip(discs_game, discs_store):
            if isinstance(disc_store, Disc) and isinstance(disc_game, Disc):
                disc_game.copy(disc_store)

        red_count = 0
        blue_count = 0
        red_spawns = self.stadium_store.red_spawn_points
        blue_spawns = self.stadium_store.blue_spawn_points
        for player in self.players:
            player.disc = get_player_disc(player.id, self.stadium_store.player_physics)
            player.disc.c_group |= (
                CollisionFlag.RED if player.team == TeamID.RED else CollisionFlag.BLUE
            )
            player.set_color()

            if player.team == TeamID.RED:
                if len(red_spawns) > 0:
                    index_red = min(red_count, len(red_spawns))
                    player.disc.position = red_spawns[index_red]
                else:
                    player.disc.position[0] = -self.stadium_game.spawn_distance
                    if (red_count % 2) == 1:
                        player.disc.position[1] = -55 * (red_count + 1 >> 1)
                    else:
                        player.disc.position[1] = 55 * (red_count + 1 >> 1)
                red_count += 1

            elif player.team == TeamID.BLUE:
                if len(blue_spawns) > 0:
                    index_blue = min(blue_count, len(blue_spawns))
                    player.disc.position = blue_spawns[index_blue]
                else:
                    player.disc.position[0] = self.stadium_game.spawn_distance
                    if (blue_count % 2) == 1:
                        player.disc.position[1] = -55 * (blue_count + 1 >> 1)
                    else:
                        player.disc.position[1] = 55 * (blue_count + 1 >> 1)
                blue_count += 1

    def start(self) -> None:
        for player in self.players:
            self.stadium_game.discs.append(player.disc)
        self.reset_discs_positions()
        if self.enable_recorder and self.recorder is not None:
            self.recorder.start()
        if self.enable_renderer and self.renderer is not None:
            self.renderer.start()

    def step(self, actions: np.ndarray) -> bool:
        for action, player in zip(actions, self.players):
            self.make_player_action(player, action)

        previous_discs_position = [
            copy.deepcopy(disc)
            for disc in self.stadium_game.discs
            if disc.c_group & CollisionFlag.SCORE != 0
        ]
        update_discs(self.stadium_game, self.players)
        resolve_collisions(self.stadium_game)
        done = self.handle_game_state(previous_discs_position)  # type: ignore
        if self.enable_recorder and self.recorder is not None:
            self.recorder.step(actions)
        if self.enable_renderer and self.renderer is not None:
            self.renderer.update()

        return done

    def stop(self, save_recording: bool) -> None:
        if self.enable_recorder and self.recorder is not None:
            self.recorder.stop(save=save_recording)

        if save_recording and self.enable_recorder and self.recorder is not None:
            log.debug(f"Recording saved under {self.recorder.filename}")
        log.debug(
            f"Game stopped with score {self.score.red}-{self.score.blue}"
            + f" at {round(self.score.time, 2)}s\n",
        )

        self.score.stop()
        self.state = GameState.KICKOFF
        self.team_kickoff = TeamID.RED
        self.stadium_game: Stadium = copy.deepcopy(self.stadium_store)
        if self.enable_recorder:
            self.recorder = GameActionRecorder(self, self.folder_rec)
        if self.enable_renderer and self.renderer is not None:
            self.renderer.stop()

    def reset(self, save_recording: bool) -> None:
        self.stop(save_recording)
        self.start()


if __name__ == "__main__":
    from ursinaxball.modules.bots import ConstantActionBot

    game = Game()
    player_physics = game.stadium_store.player_physics

    custom_score = GameScore(time_limit=1, score_limit=1)
    game.score = custom_score

    bot_1 = ConstantActionBot([1, 0, 0])
    bot_2 = ConstantActionBot([1, 1, 1], symmetry=True)

    player_red = PlayerHandler("P0", player_physics, TeamID.RED, bot=bot_1)
    player_blue = PlayerHandler("P1", player_physics, TeamID.BLUE, bot=bot_2)
    game.add_players([player_red, player_blue])

    game.start()

    done = False
    while not done:
        actions_player_1 = player_red.step(game)
        actions_player_2 = player_blue.step(game)
        done = game.step(np.array([actions_player_1, actions_player_2]))

    game.stop(save_recording=False)
