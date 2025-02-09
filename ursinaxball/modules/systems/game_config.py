import logging
from dataclasses import dataclass

from ursinaxball.common_values import BaseMap


@dataclass
class GameConfig:
    """Configuration class for the game settings."""

    stadium_file: str = BaseMap.CLASSIC
    folder_rec: str = ""
    logging_level: int = logging.DEBUG
    enable_vsync: bool = True
    enable_renderer: bool = True
    fov: int = 550
    enable_recorder: bool = True

    def __post_init__(self):
        logging.basicConfig(
            level=self.logging_level, format="%(levelname)s - %(message)s"
        )
