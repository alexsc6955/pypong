"""
Paddle class for DejaBounce
"""

from __future__ import annotations

from mini_arcade_core import Backend, SpriteEntity

from deja_bounce.utils import logger


class Paddle(SpriteEntity):
    """
    Paddle entity using mini-arcade-core's SpriteEntity.
    """

    def __init__(
        self, x: float, y: float, width: int, height: int, window_height: int
    ):
        super().__init__(x=x, y=y, width=width, height=height)
        self.window_height = window_height
        self.speed = 300.0
        self.moving_up = False
        self.moving_down = False

        logger.info("Paddle created")

    def update(self, dt: float) -> None:  # override Entity.update
        if self.moving_up:
            self.y -= self.speed * dt
        if self.moving_down:
            self.y += self.speed * dt

        # Clamp inside window
        if self.y < 0:
            self.y = 0
        if self.y + self.height > self.window_height:
            self.y = self.window_height - self.height

    def draw(self, surface: Backend) -> None:  # override Entity.draw
        surface.draw_rect(int(self.x), int(self.y), self.width, self.height)
