import importlib.resources as pkg_resources
import json

from ursinaxball.game import stadiums
from ursinaxball.game.common_values import DICT_COLLISION, DICT_KEYS, CollisionFlag


def rename_keys(data: dict):
    for key in DICT_KEYS:
        if key in data:
            data[DICT_KEYS[key]] = data.pop(key)
    return data


def parse_collision(collision: list[str]):
    collision_flag = CollisionFlag.NONE
    for c in collision:
        collision_flag |= DICT_COLLISION[c]
    return collision_flag


def parse_collision_properties(data: dict):
    if "collision_group" in data:
        data["collision_group"] = parse_collision(data.get("collision_group", []))
    if "collision_mask" in data:
        data["collision_mask"] = parse_collision(data.get("collision_mask", []))
    return data


def reformat_traits(data: dict):
    traits_list = []
    for key, value in data["traits"].items():
        value["name"] = key
        traits_list.append(value)
    return traits_list


def parse_trait(data: dict):
    data = parse_collision_properties(data)
    return data


def parse_vertex(data: dict):
    data = parse_collision_properties(data)
    data["position"] = [data.pop("x"), data.pop("y")]
    return data


def parse_plane(data: dict):
    data = parse_collision_properties(data)
    return data


def parse_segment(data: dict):
    data = parse_collision_properties(data)
    data["vertices_index"] = [data.pop("v0"), data.pop("v1")]
    return data


def parse_goal(data: dict):
    data["points"] = [data.pop("p0"), data.pop("p1")]
    data["team"] = 1 if data["team"] == "red" else 2
    return data


def parse_stadium(data: dict):
    data["vertices"] = [parse_vertex(vertex) for vertex in data.get("vertices")]
    data["goals"] = [parse_goal(goal) for goal in data.get("goals")]
    data["segments"] = [parse_segment(segment) for segment in data.get("segments")]
    data["traits"] = reformat_traits(data)
    data["traits"] = [parse_trait(trait) for trait in data.get("traits")]
    return data


if __name__ == "__main__":
    file_name = "classic.hbs"
    with pkg_resources.open_text(stadiums, file_name) as f:
        res = json.loads(f.read(), object_hook=rename_keys)
        res = parse_stadium(res)
        print(json.dumps(res["traits"], indent=4))
