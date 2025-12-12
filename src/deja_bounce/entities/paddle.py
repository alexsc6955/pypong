"""
Paddle class for DejaBounce
"""

from __future__ import annotations

from dataclasses import dataclass

from mini_arcade_core import KinematicData, KinematicEntity, Position2D, Size2D

from deja_bounce.utils import logger

from .common import RectDrawMixin


@dataclass
class PaddleConfig:
    """
    Configuration for Paddle entity.
    """

    position: Position2D
    size: Size2D
    window_height: int
    speed: float = 300.0


class Paddle(RectDrawMixin, KinematicEntity):
    """
    Paddle entity using mini-arcade-core's SpriteEntity.
    """

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, config: PaddleConfig):
        data = KinematicData.rect(
            x=config.position.x,
            y=config.position.y,
            width=config.size.width,
            height=config.size.height,
            vx=0.0,
            vy=0.0,
        )
        super().__init__(data)
        self.window_height = config.window_height
        self.speed = config.speed
        self.moving_up = False
        self.moving_down = False
        self.vy = 0.0

        logger.info("Paddle created")

    def update(self, dt: float) -> None:  # override Entity.update
        """
        Update paddle position based on input flags.

        :param dt: Delta time since last update.
        :type dt: float
        """
        # Configure vertical velocity from input flags
        if self.moving_up:
            self.velocity.move_up(self.speed)
        elif self.moving_down:
            self.velocity.move_down(self.speed)
        else:
            self.velocity.stop_y()

        # Apply velocity to position (uses Velocity2D.advance under the hood)
        super().update(dt)

        # Expose current vy for the paddle influence logic
        self.vy = self.velocity.vy

        # Clamp inside window and kill velocity if we hit borders
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.stop_y()

        if self.position.y + self.size.height > self.window_height:
            self.position.y = self.window_height - self.size.height
            self.velocity.stop_y()
