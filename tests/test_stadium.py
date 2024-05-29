from ursinaxball.objects import load_stadium
from ursinaxball.utils.enums import BaseMap


def test_stadium():
    haxball_map = BaseMap.CLASSIC
    stadium = load_stadium(haxball_map)
    assert stadium.name == "Classic"
