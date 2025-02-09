# Ursinaxball

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ursinaxball is a Python clone of the game [HaxBall](https://www.haxball.com) developed with the Ursina game engine. It provides a flexible game engine for creating physics-based soccer games with customizable rules and bot support.

## Features

- Physics-based gameplay with realistic ball and player movement
- Team-based gameplay (Red vs Blue teams)
- Customizable stadium layouts
- Bot AI system with different complexity levels
- Game recording and replay system
- Configurable rendering settings
- Score tracking and game state management

## Requirements

- Python >= 3.9, < 3.13
- Dependencies managed via Poetry

## Installation

1. Install Poetry if you haven't already:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. Install the library:

    ```bash
    poetry add ursinaxball
    ```

## Quick Start

Here's a minimal example to get started:

```python
from ursinaxball import Game
from ursinaxball.game import GameConfig
from ursinaxball.common_values import BaseMap

# Configure the game
config = GameConfig(
    stadium_file=BaseMap.CLASSIC,
    enable_vsync=True,
    fov=550
)

# Create and start the game
game = Game(config=config)

# Add players and start playing!
# See example.py for a complete implementation
```

## Configuration

The game can be configured using the `GameConfig` class:

```python
@dataclass
class GameConfig:
    stadium_file: str = BaseMap.CLASSIC    # Stadium layout file
    folder_rec: str = ""                   # Recording folder path
    logging_level: int = logging.DEBUG     # Logging verbosity
    enable_vsync: bool = True              # VSync for rendering
    enable_renderer: bool = True           # Enable/disable rendering
    fov: int = 550                        # Field of view
    enable_recorder: bool = True           # Enable/disable game recording
```

## Examples

Check out the example files in the repository:

- `example.py`: Basic game with keyboard controls and a bot
- `example_multi.py`: Multiplayer example
- `play_obstacle.py`: Example with custom stadium layout

## Development

1. Clone the repository:

    ```bash
    git clone https://github.com/HaxballGym/ursinaxball.git
    cd ursinaxball
    ```

2. Install development dependencies:

    ```bash
    poetry install --with dev
    ```

3. Run tests:

    ```bash
    poetry run pytest
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original HaxBall game: <www.haxball.com>
- Ursina game engine: <www.ursinaengine.org>
