from __future__ import annotations

from mini_arcade_core import GameConfig, run_game
from mini_arcade_native_backend import NativeBackend

from deja_bounce.constants import FPS, WINDOW_SIZE
from deja_bounce.scenes import PongScene


def main():
    """Main entry point for PyPong."""
    backend = NativeBackend()
    width, height = WINDOW_SIZE
    config = GameConfig(
        width=width,
        height=height,
        title="PyPong (Native SDL2 + mini-arcade-core)",
        fps=FPS,
        backend=backend,
    )
    run_game(PongScene, config=config)


if __name__ == "__main__":
    main()
