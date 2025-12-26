"""
Overlay scenes for Deja Bounce.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mini_arcade_core.backend import Backend
from mini_arcade_core.spaces.d2 import Size2D
from mini_arcade_core.ui import BaseOverlay

from deja_bounce.constants import WHITE
from deja_bounce.scenes.models import PongModel
from deja_bounce.utils import logger

if TYPE_CHECKING:
    from deja_bounce.scenes.pong import PongScene


class PhotoOverlay(BaseOverlay):
    """
    Overlay for photo mode.
    """

    def __init__(self, model: PongModel):
        self.model = model

    def draw(self, surface: "Backend"):
        if not self.model.photo_mode:
            return

        x, y = 20, 60
        surface.draw_text(x, y, "Deja Bounce", color=(155, 155, 255))
        surface.draw_text(
            x, y + 30, "Finding the twist", color=(155, 155, 255)
        )
        surface.draw_text(x, y + 60, "in a Pong-like", color=(155, 155, 255))


class ScoreOverlay(BaseOverlay):
    """Simple overlay to draw the score."""

    def __init__(self, model: PongModel, size: Size2D):
        self.model = model
        self.size = size

    def draw(self, surface: Backend):
        score_y = 20
        surface.draw_text(
            self.size.width // 4,
            score_y,
            str(self.model.score.left),
            color=WHITE,
        )
        surface.draw_text(
            self.size.width * 3 // 4,
            score_y,
            str(self.model.score.right),
            color=WHITE,
        )


class WallsOverlay(BaseOverlay):
    """
    Simple overlay to draw walls.
    """

    def __init__(self, model: PongModel, size: Size2D):
        self.model = model
        self.size = size

    def _middle_line(self, surface: Backend):
        line_width = 5
        x = self.size.width // 2 - line_width // 2
        y = 0
        h = self.size.height
        # Color gray
        surface.draw_rect(x, y, line_width, h, color=(150, 150, 150))

    def draw(self, surface: Backend):
        wall_height = self.model.wall_height
        w = self.size.width
        h = self.size.height

        # Middle line
        self._middle_line(surface)
        # Top wall
        surface.draw_rect(0, 0, w, wall_height, color=WHITE)
        # Bottom wall
        surface.draw_rect(0, h - wall_height, w, wall_height, color=WHITE)

        if self.model.wall_left:
            # Left wall
            surface.draw_rect(0, 0, wall_height, h, color=WHITE)

        if self.model.wall_right:
            # Right wall
            logger.critical("Drawing right wall")
            surface.draw_rect(w - wall_height, 0, wall_height, h, color=WHITE)
            surface.draw_rect(w - wall_height, 0, wall_height, h, color=WHITE)
