"""
Minimal CPU paddle controller for Deja Bounce.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal

from deja_bounce.entities import Ball, Paddle

Side = Literal["LEFT", "RIGHT"]


@dataclass
class CpuConfig:
    """
    Basic CPU difficulty settings.

    - max_speed: how fast the CPU paddle can move (units/sec)
    - dead_zone: how close to the ball center before it stops moving
    """

    max_speed: float = 65.0  # slower = easier
    dead_zone: float = (
        16.0  # larger dead_zone = CPU "overshoots" less, more human = easier
    )
    reaction_distance: float = 180.0
    error_margin: float = 24.0


class CpuPaddleController:
    """
    Very simple CPU:
    - Looks at the ball's center Y.
    - Moves paddle up/down to follow it, clamped by max_speed.
    """

    def __init__(
        self,
        paddle: Paddle,
        ball: Ball,
        side: Side = "RIGHT",
        config: CpuConfig | None = None,
    ):
        """
        :param paddle: The paddle to control.
        :type paddle: Paddle

        :param ball: The ball to track.
        :type ball: Ball

        :param config: The CPU configuration settings.
        :type config: CpuConfig, optional
        """
        self.paddle = paddle
        self.ball = ball
        self.side = side
        self.config = config or CpuConfig()

        # Make sure paddle speed matches CPU config so movement feels consistent
        self.paddle.speed = self.config.max_speed
        self._aim_offset_y = self._new_offset()

    def _new_offset(self) -> float:
        # vertical error in [-error_margin, error_margin]
        m = self.config.error_margin
        return random.uniform(-m, m) if m > 0 else 0.0

    def _stop(self):
        self.paddle.moving_up = False
        self.paddle.moving_down = False

    # Justification: dt is unused but kept for interface consistency
    # pylint: disable=unused-argument
    def update(self, dt: float):
        """
        Update CPU paddle movement based on ball position.

        :param dt: Delta time since last update (unused).
        :type dt: float
        """
        vx = self.ball.velocity.vx

        # React only when ball is coming toward THIS paddle
        if self.side == "RIGHT" and vx <= 0:
            self._stop()
            return
        if self.side == "LEFT" and vx >= 0:
            self._stop()
            return

        # Distance-to-react should be side-correct
        if self.side == "RIGHT":
            distance_x = self.paddle.position.x - (
                self.ball.position.x + self.ball.size.width
            )
        else:  # LEFT
            distance_x = self.ball.position.x - (
                self.paddle.position.x + self.paddle.size.width
            )

        if distance_x > self.config.reaction_distance:
            self._stop()
            return

        # Y aiming (same as you already have)
        ball_center = (
            self.ball.position.y
            + self.ball.size.height / 2
            + self._aim_offset_y
        )
        paddle_center = self.paddle.position.y + self.paddle.size.height / 2
        diff = ball_center - paddle_center

        if abs(diff) < self.config.dead_zone:
            self._stop()
            return

        if diff < 0:
            self.paddle.moving_up = True
            self.paddle.moving_down = False
        else:
            self.paddle.moving_up = False
            self.paddle.moving_down = True
