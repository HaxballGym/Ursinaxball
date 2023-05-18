from ursinaxball.common_values import BaseMap
from ursinaxball.objects import load_stadium_hbs


def test_stadium():
    haxball_map = BaseMap.CLASSIC
    stadium = load_stadium_hbs(haxball_map)
    print(stadium.name)
