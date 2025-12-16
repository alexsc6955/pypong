"""
Minimal main application for Deja Bounce.
"""

from __future__ import annotations

from mini_arcade_core import GameConfig, SceneRegistry, run_game
from mini_arcade_native_backend import NativeBackend

from deja_bounce.constants import ASSETS_ROOT, FPS, WINDOW_SIZE
from deja_bounce.scenes import (
    MenuScene,
    menu_scene_factory,
    pause_scene_factory,
    pong_scene_factory,
)


def run():
    """Main entry point for DejaBounce."""
    registry = SceneRegistry(_factories={})
    registry.register("menu", menu_scene_factory)
    registry.register("pong", pong_scene_factory)
    registry.register("pause", pause_scene_factory)

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
    run_game(MenuScene, config=config, registry=registry)


if __name__ == "__main__":
    run()
    run()

if __name__ == "__main__":
    run()
    run()
