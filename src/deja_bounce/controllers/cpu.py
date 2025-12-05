from __future__ import annotations

from dataclasses import dataclass

from deja_bounce.entities import Ball, Paddle


@dataclass
class CpuConfig:
    """
    Basic CPU difficulty settings.

    - max_speed: how fast the CPU paddle can move (units/sec)
    - dead_zone: how close to the ball center before it stops moving
    """

    max_speed: float = 260.0  # slower = easier
    dead_zone: float = (
        4.0  # larger dead_zone = CPU "overshoots" less, more human
    )


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
        config: CpuConfig | None = None,
    ) -> None:
        self.paddle = paddle
        self.ball = ball
        self.config = config or CpuConfig()

        # Make sure paddle speed matches CPU config so movement feels consistent
        self.paddle.speed = self.config.max_speed

    def update(self, dt: float) -> None:
        target_y = self.ball.y + self.ball.height / 2
        center_y = self.paddle.y + self.paddle.height / 2
        diff = target_y - center_y

        # dead zone: don't jitter when we're basically aligned
        if abs(diff) < self.config.dead_zone:
            self.paddle.moving_up = False
            self.paddle.moving_down = False
            return

        # Decide direction: up if ball is above, down if below
        if diff < 0:
            self.paddle.moving_up = True
            self.paddle.moving_down = False
        else:
            self.paddle.moving_up = False
            self.paddle.moving_down = True
