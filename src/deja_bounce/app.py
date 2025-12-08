"""
Minimal main application for Deja Bounce.
"""

from __future__ import annotations

from mini_arcade_core import GameConfig, run_game
from mini_arcade_native_backend import NativeBackend

from deja_bounce.constants import FPS, ASSETS_ROOT, WINDOW_SIZE
from deja_bounce.scenes import MenuScene


def main():
    """Main entry point for DejaBounce."""
    font_path = ASSETS_ROOT / "fonts" / "deja_vu_dive" / "Deja-vu_dive.ttf"

    backend = NativeBackend(font_path=str(font_path), font_size=24)
    width, height = WINDOW_SIZE
    config = GameConfig(
        width=width,
        height=height,
        title="DejaBounce (Native SDL2 + mini-arcade-core)",
        fps=FPS,
        backend=backend,
    )
    run_game(MenuScene, config=config)


if __name__ == "__main__":
    main()
