"""
This module defines the Ball class.
"""

from __future__ import annotations

from mini_arcade_core import Backend, SpriteEntity

from .utils import logger


class Ball(SpriteEntity):
    """
    Ball entity using SpriteEntity.
    """

    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x=x, y=y, width=width, height=height)
        self.vx = 250.0
        self.vy = 200.0

        logger.info("Ball created")

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface: Backend) -> None:
        surface.draw_rect(int(self.x), int(self.y), self.width, self.height)
