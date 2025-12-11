"""
Paddle class for DejaBounce
"""

from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core import Backend, Position2D, Size2D, SpriteEntity

from deja_bounce.utils import logger


@dataclass
class PaddleConfig:
    """
    Configuration for Paddle entity.
    """

    position: Position2D
    size: Size2D
    window_height: int
    speed: float = 300.0


class Paddle(SpriteEntity):
    """
    Paddle entity using mini-arcade-core's SpriteEntity.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, config: PaddleConfig):
        super().__init__(config.position, config.size)
        self.window_height = config.window_height
        self.speed = config.speed
        self.moving_up = False
        self.moving_down = False
        self.vy = 0.0

        logger.info("Paddle created")

    def update(self, dt: float) -> None:  # override Entity.update
        # compute instantaneous vertical velocity based on input flags
        vy = 0.0
        if self.moving_up:
            vy = -self.speed
        elif self.moving_down:
            vy = self.speed

        # apply movement
        self.position.y += vy * dt
        self.vy = vy  # <--- store for inertia

        # Clamp inside window
        self.position.y = max(self.position.y, 0)
        if self.position.y + self.size.height > self.window_height:
            self.position.y = self.window_height - self.size.height

    def draw(self, surface: Backend) -> None:  # override Entity.draw
        surface.draw_rect(
            int(self.position.x),
            int(self.position.y),
            self.size.width,
            self.size.height,
        )
