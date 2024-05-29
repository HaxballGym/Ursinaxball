from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from pyinstrument import Profiler
from pyperf import Benchmark, Runner

from ursinaxball import Game
from ursinaxball.modules import GameScore, PlayerHandler
from ursinaxball.utils.enums import BaseMap, TeamID


def init_game(enable_renderer: bool) -> Game:
    game = Game(
        folder_rec="./recordings/",
        enable_vsync=False,
        stadium_file=BaseMap.CLASSIC,
        enable_renderer=enable_renderer,
    )
    game.score = GameScore(time_limit=1)

    player_red = PlayerHandler("P1", TeamID.RED)
    player_blue = PlayerHandler("P2", TeamID.BLUE)
    game.add_players([player_red, player_blue])
    game.reset(save_recording=False)

    return game


def init_game_obstacle(enable_renderer: bool) -> Game:
    game = Game(
        folder_rec="./recordings/",
        enable_vsync=False,
        stadium_file=BaseMap.OBSTACLE_WINKY,
        enable_renderer=enable_renderer,
    )
    game.score = GameScore(time_limit=1)

    player_red = PlayerHandler("P1", TeamID.RED)
    game.add_players([player_red])
    game.reset(save_recording=False)

    return game


def generate_random_actions(rng: np.random.Generator):
    array_1 = rng.integers(-1, 2, size=2)
    array_2 = rng.integers(0, 2, size=1)
    return np.concatenate((array_1, array_2))


def single_game():
    game = init_game(enable_renderer=False)
    rng = np.random.default_rng(12345)
    nb_frames = 60 * 60 * 1  # 1 minute

    for _ in range(nb_frames):
        actions_0 = generate_random_actions(rng)
        actions_1 = generate_random_actions(rng)
        actions = np.stack((actions_0, actions_1))
        game.step(actions)


def single_game_pyinstrument():
    profiler = Profiler()
    profiler.start()

    single_game()

    profiler.stop()
    html = profiler.output_html()
    with Path.open(PATH_PROJECT / "benchmarks/single_game_pyinstrument.html", "w") as f:
        f.write(html)


def single_game_pyperf():
    runner = Runner()
    res_pyperf = runner.bench_func(name="single_game", func=single_game)

    assert isinstance(res_pyperf, Benchmark)
    output_path = PATH_PROJECT / "benchmarks/single_game_pyperf.html"
    output_pyperf(res_pyperf, output_path)


def multiple_games(n=5):
    game = init_game(enable_renderer=False)
    rng = np.random.default_rng(12345)
    nb_frames = 60 * 60 * 1  # 1 minute

    for _ in range(n):
        for _ in range(nb_frames):
            actions_0 = generate_random_actions(rng)
            actions_1 = generate_random_actions(rng)
            actions = np.stack((actions_0, actions_1))
            game.step(actions)
        game.reset(save_recording=False)


def multiple_games_pyperf(n=5):
    runner = Runner()
    res_pyperf = runner.bench_func(
        name="multiple_games", func=multiple_games, args=(n,)
    )

    assert isinstance(res_pyperf, Benchmark)
    output_path = PATH_PROJECT / "benchmarks/multiple_games_pyperf.html"
    output_pyperf(res_pyperf, output_path)


def multiple_games_pyinstrument(n=5):
    profiler = Profiler()
    profiler.start()

    multiple_games(n)

    profiler.stop()
    html = profiler.output_html()
    with Path.open(
        PATH_PROJECT / "benchmarks/multiple_games_pyinstrument.html", "w"
    ) as f:
        f.write(html)


def obstacle_map():
    game = init_game_obstacle(enable_renderer=False)

    rng = np.random.default_rng(54321)
    nb_frames = 60 * 30 * 1  # 1 minute

    for _ in range(nb_frames):
        actions = np.stack((generate_random_actions(rng),))
        game.step(actions)


def obstacle_map_pyperf():
    runner = Runner()
    res_pyperf = runner.bench_func(name="obstacle_map", func=obstacle_map)

    assert isinstance(res_pyperf, Benchmark)

    path_output = PATH_PROJECT / "benchmarks/obstacle_map_pyperf.html"
    output_pyperf(res_pyperf, path_output)


def obstacle_map_pyinstrument():
    profiler = Profiler()
    profiler.start()
    obstacle_map()
    profiler.stop()
    html = profiler.output_html()

    with Path.open(
        PATH_PROJECT / "benchmarks/obstacle_map_pyinstrument.html", "w"
    ) as f:
        f.write(html)


def output_pyperf(bench: Benchmark, output_path: Path):
    values = bench.get_values()

    if len(values) == 0:
        return

    mean = bench.mean()
    std = bench.stdev()

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=values,
            name="Benchmark results",
            nbinsx=25,
        )
    )

    fig.add_vline(
        x=mean,
        line_width=3,
        line_dash="dash",
        line_color="green",
        annotation={"text": f"mean: {mean:.2f}s"},
    )
    fig.add_vline(
        x=mean + std,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation={"text": f"mean + std: {(mean + std):.2f}s"},
    )
    fig.add_vline(
        x=mean - std,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation={"text": f"mean - std: {(mean - std):.2f}s"},
    )

    fig.update_layout(
        title_text="Benchmark results",
        xaxis_title_text="Time (s)",
        yaxis_title_text="Count",
        bargap=0.01,
    )

    fig.write_html(output_path.as_posix())


def main():
    obstacle_map_pyinstrument()
    obstacle_map_pyperf()


if __name__ == "__main__":
    main()
