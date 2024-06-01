from pathlib import Path

PATH_PACKAGE = Path(__file__).parents[2]
PATH_PROJECT = Path(__file__).parents[1]
PATH_STADIUMS = PATH_PROJECT / "stadiums"
PATH_RECORDINGS = PATH_PACKAGE / "recordings"

BACKGROUND_FILL_COLORS = {
    "grass": "C7E6BD",
    "hockey": "E9CC6E",
    "none": "000000",
}

BACKGROUND_BORDER_COLORS = {
    "grass": "718C5A",
    "hockey": "555555",
    "none": "000000",
}
