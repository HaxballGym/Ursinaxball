from ursina import Entity, Ursina, Vec2, camera, color, destroy, window

from ursinaxball.objects.base import Disc


class GameRenderer(object):
    def __init__(self, game, enable_vsync=True) -> None:
        self.game = game
        self.app: Ursina = None
        self.disc_entities = []
        self.segment_entities = []
        self.background_entities = []
        self.UI_strings = []
        self.UI_fixed_entities = []
        self.enable_vsync = enable_vsync

    def get_disc_player(self, disc: Disc):
        if not hasattr(disc, "player_id"):
            return None
        return self.game.get_player_by_id(disc.player_id)

    def handle_shooting(self, disc: Disc, entity: Entity) -> None:
        player = self.get_disc_player(disc)
        if player is None:
            return
        if player.is_kicking():
            entity.children[0].color = color.white
        else:
            entity.children[0].color = color.black

    def start(self) -> None:

        if self.app is None:
            window.borderless = False
            window.vsync = self.enable_vsync

            self.app = Ursina(
                title="HaxballGym",
            )
            self.UI_fixed_entities = self.game.score.get_fixed_entities()

        window.exit_button.visible = False
        camera.orthographic = True
        camera.position = Vec2(0, 0)
        camera.fov = 550

        self.disc_entities = [
            disc.get_entity() for disc in self.game.stadium_game.discs
        ]
        self.segment_entities = [
            segment.get_entity() for segment in self.game.stadium_game.segments
        ]
        self.background_entities = self.game.stadium_game.background.get_entities()
        self.UI_strings = self.game.score.get_string_entities()

        self.app.step()

    def update(self):
        for entity, game_disc in zip(self.disc_entities, self.game.stadium_game.discs):
            entity.position = game_disc.position
            self.handle_shooting(game_disc, entity)

        if self.UI_strings[0].text != self.game.score.get_score_string():
            self.UI_strings[0].text = self.game.score.get_score_string()
        if self.UI_strings[1].text != self.game.score.get_time_string():
            self.UI_strings[1].text = self.game.score.get_time_string()

        self.app.step()

    def stop(self):
        # destroy all entities created by this renderer
        for entity in (
            self.disc_entities
            + self.segment_entities
            + self.background_entities
            + self.UI_strings
        ):
            destroy(entity)
