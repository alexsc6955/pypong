"""
Minimal Pong-like scene using mini-arcade-core.
"""

from __future__ import annotations

from mini_arcade_core import (
    Backend,
    Event,
    EventType,
    Game,
    Scene,
    SpriteEntity,
)

from deja_bounce.constants import PADDLE_SIZE
from deja_bounce.controllers import CpuConfig, CpuPaddleController
from deja_bounce.entities import Ball, Paddle
from deja_bounce.utils import logger


class PongScene(Scene):
    """
    Minimal scene: opens a window, clears screen, handles quit/ESC.
    """

    def __init__(self, game: Game):
        super().__init__(game)
        self.width = game.config.width
        self.height = game.config.height
        pad_w, pad_h = PADDLE_SIZE

        self.left = Paddle(
            x=20,
            y=self.height / 2 - pad_h / 2,
            width=pad_w,
            height=pad_h,
            window_height=self.height,
        )
        self.right = Paddle(
            x=self.width - 20 - pad_w,
            y=self.height / 2 - pad_h / 2,
            width=pad_w,
            height=pad_h,
            window_height=self.height,
        )

        self.ball = Ball(
            x=self.width / 2 - 5,
            y=self.height / 2 - 5,
            width=10,
            height=10,
        )

        self.entities: list[SpriteEntity] = [self.left, self.right, self.ball]

        self.left_score = 0
        self.right_score = 0

        cpu_cfg = CpuConfig(max_speed=260.0, dead_zone=4.0)
        self.cpu = CpuPaddleController(self.right, self.ball, config=cpu_cfg)

    def on_enter(self):
        logger.info("PongScene on_enter")

    def on_exit(self):
        logger.info("PongScene on_exit")

    def handle_event(self, event: Event):  # type: ignore[override]
        """
        Handle backend events (mini_arcade_core.Event).
        """
        if event.type == EventType.QUIT:
            logger.info("Quit event received")
            self.game.quit()
            return

        if event.type == EventType.KEYDOWN:
            logger.debug(f"Key down: {event.key}")
            if event.key == 27:  # ESC
                logger.info("ESC pressed, quitting")
                self.game.quit()
                return

            # Left paddle: W / S
            if event.key == ord("w"):
                self.left.moving_up = True
            if event.key == ord("s"):
                self.left.moving_down = True

        elif event.type == EventType.KEYUP:
            if event.key == ord("w"):
                self.left.moving_up = False
            if event.key == ord("s"):
                self.left.moving_down = False

    def update(self, dt: float):
        """
        Update game logic. (None yet.)
        """
        for ent in self.entities:
            ent.update(dt)

        self.cpu.update(dt)

        # Top/bottom bounce
        if self.ball.y <= 0:
            self.ball.y = 0
            self.ball.vy *= -1

        if self.ball.y + self.ball.height >= self.height:
            self.ball.y = self.height - self.ball.height
            self.ball.vy *= -1

        # Paddle collisions
        if self._intersects(self.ball, self.left):
            self.ball.x = self.left.x + self.left.width
            self.ball.vx *= -1

        if self._intersects(self.ball, self.right):
            self.ball.x = self.right.x - self.ball.width
            self.ball.vx *= -1

        # Scoring – ball leaves left/right
        if self.ball.x < 0:
            self.right_score += 1
            logger.info(
                f"Right scores! {self.left_score} - {self.right_score}"
            )
            self._reset_ball(direction=1)

        if self.ball.x > self.width:
            self.left_score += 1
            logger.info(f"Left scores! {self.left_score} - {self.right_score}")
            self._reset_ball(direction=-1)

    def draw(self, surface: Backend):  # type: ignore[override]
        """
        Draw the frame using the Backend as the 'surface'.
        """
        # We assume backend.begin_frame/end_frame is handled by Game.
        # Here we just draw the center line like in the original Pong.
        line_width = 5
        x = self.width // 2 - line_width // 2
        y = 0
        h = self.height

        surface.draw_rect(x, y, line_width, h)

        # Draw all entities
        for ent in self.entities:
            ent.draw(surface)

    @staticmethod
    def _intersects(ball: Ball, paddle: Paddle) -> bool:
        return not (
            ball.x + ball.width < paddle.x
            or ball.x > paddle.x + paddle.width
            or ball.y + ball.height < paddle.y
            or ball.y > paddle.y + paddle.height
        )

    def _reset_ball(self, direction: int):
        """
        Reset ball to center, heading left (-1) or right (+1).
        """
        self.ball.x = self.width / 2 - self.ball.width / 2
        self.ball.y = self.height / 2 - self.ball.height / 2
        self.ball.vx = 250.0 * direction
        self.ball.vy = 200.0
