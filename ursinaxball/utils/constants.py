from pathlib import Path

PATH_PACKAGE = Path(__file__).parents[2]
PATH_PROJECT = Path(__file__).parents[1]
PATH_STADIUMS = PATH_PROJECT / "stadiums"
PATH_RECORDINGS = PATH_PACKAGE / "recordings"

GRASS_BORDER_COLOR = "C7E6BD"
HOCKEY_BORDER_COLOR = "E9CC6E"
DEFAULT_BORDER_COLOR = "000000"

GRASS_FILL_COLOR = "718C5A"
HOCKEY_FILL_COLOR = "555555"
DEFAULT_FILL_COLOR = "000000"
