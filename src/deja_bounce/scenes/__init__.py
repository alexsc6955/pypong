"""
Scene modules for Deja Bounce.
"""

# TODO: Refactor cyclic imports later. (MenuScene <-> PongScene)
# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import
from __future__ import annotations

from .menu import MenuScene, menu_scene_factory
from .pause import PauseScene, pause_scene_factory
from .pong import PongScene, pong_scene_factory

__all__ = [
    "PongScene",
    "pong_scene_factory",
    "MenuScene",
    "menu_scene_factory",
    "PauseScene",
    "pause_scene_factory",
]

# pylint: enable=cyclic-import
