"""
Scene modules for Deja Bounce.
"""

# TODO: Refactor cyclic imports later. (MenuScene <-> PongScene)
# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import
from __future__ import annotations

from .menu import MenuScene
from .pong import PongScene

__all__ = ["PongScene", "MenuScene"]

# pylint: enable=cyclic-import
