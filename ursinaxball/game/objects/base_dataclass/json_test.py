import importlib.resources as pkg_resources
from pprint import pprint
from ursinaxball.game import stadiums
import json
from cattr import structure, unstructure
from ursinaxball.game.common_values import DICT_KEYS


def rename_keys(data: dict):
    for key in DICT_KEYS:
        if key in data:
            data[DICT_KEYS[key]] = data.pop(key)
    return data


def parse_vertex(data: dict):
    data["position"] = [data.pop("x"), data.pop("y")]
    return data


def parse_goal(data: dict):
    data["points"] = [data.pop("p0"), data.pop("p1")]
    data["team"] = 1 if data["team"] == "red" else 2
    return data


def parse_stadium(data: dict):
    data["vertices"] = [parse_vertex(vertex) for vertex in data.get("vertices")]
    data["goals"] = [parse_goal(goal) for goal in data.get("goals")]
    return data


if __name__ == "__main__":
    file_name = "classic.hbs"
    with pkg_resources.open_text(stadiums, file_name) as f:
        res = json.loads(f.read(), object_hook=rename_keys)
        res = parse_stadium(res)
        print(json.dumps(res["traits"], indent=4))
