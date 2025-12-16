"""
Minimal Pong-like scene using mini-arcade-core.
"""

# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import

from __future__ import annotations

from collections import deque

from mini_arcade_core import (
    Backend,
    Bounds2D,
    Event,
    EventType,
    Game,
    Key,
    KinematicData,
    Position2D,
    Scene,
    Size2D,
    VerticalBounce,
)

from deja_bounce.constants import PADDLE_SIZE, ROOT, WHITE
from deja_bounce.controllers import CpuConfig, CpuPaddleController
from deja_bounce.entities import Ball, Paddle, PaddleConfig
from deja_bounce.utils import logger


# pylint: disable=too-many-instance-attributes
class PongScene(Scene):
    """
    Minimal scene: opens a window, clears screen, handles quit/ESC.
    """

    right_paddle: Paddle
    left_paddle: Paddle
    ball: Ball

    def __init__(self, game: Game):
        super().__init__(game)

        self.bounds = Bounds2D.from_size(self.size)
        self.ball_vertical_bounds = VerticalBounce(self.bounds)

        self._set_entities()

        self.left_score = 0
        self.right_score = 0

        cpu_cfg = CpuConfig(max_speed=260.0, dead_zone=4.0)
        self.cpu = CpuPaddleController(
            self.right_paddle, self.ball, config=cpu_cfg
        )

        self.trail_enabled = False
        self.trail = deque(maxlen=15)

        self.photo_mode = False
        self.add_overlay(self._photo_overlay)

    def _set_entities(self):
        pad_w, pad_h = PADDLE_SIZE

        # Left paddle
        self.left_paddle = Paddle(
            PaddleConfig(
                position=Position2D(20, self.size.height / 2 - pad_h / 2),
                size=Size2D(pad_w, pad_h),
                window_height=self.size.height,
            )
        )

        # Right paddle
        self.right_paddle = Paddle(
            PaddleConfig(
                position=Position2D(
                    self.size.width - 20 - pad_w,
                    self.size.height / 2 - pad_h / 2,
                ),
                size=Size2D(pad_w, pad_h),
                window_height=self.size.height,
            )
        )

        # Ball
        self.ball = Ball(
            KinematicData.rect(
                x=self.size.width / 2 - 5,
                y=self.size.height / 2 - 5,
                width=10,
                height=10,
                vx=250.0,
                vy=200.0,
            )
        )

        self.add_entity(self.left_paddle, self.right_paddle, self.ball)

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

            if event.key == Key.T:
                self.trail_enabled = not self.trail_enabled

            if event.key == Key.P:
                # toggle photo mode; ensure trail on when enabled
                self.photo_mode = not self.photo_mode
                if self.photo_mode:
                    self.trail_enabled = True

            if event.key == Key.F12:
                self.game.screenshot(
                    "screenshot.bmp", str(ROOT / "screenshots")
                )
                logger.info("Screenshot saved: screenshot.bmp")
                return

            if event.key == Key.ESCAPE:  # ESC
                self.game.push_scene("pause", as_overlay=True)
                return

            # Left paddle: W / S
            if event.key == Key.W:
                self.left_paddle.moving_up = True
            if event.key == Key.S:
                self.left_paddle.moving_down = True

        elif event.type == EventType.KEYUP:
            if event.key == Key.W:
                self.left_paddle.moving_up = False
            if event.key == Key.S:
                self.left_paddle.moving_down = False

    def update(self, dt: float):
        """
        Update game logic. (None yet.)
        """
        self.update_entities(dt)
        self.cpu.update(dt)

        # Top/bottom bounce
        self.ball_vertical_bounds.apply(self.ball)

        # Paddle collisions
        if self.ball.collider.intersects(self.left_paddle.collider):
            self.ball.position.x = (
                self.left_paddle.position.x + self.left_paddle.size.width
            )
            self.ball.velocity.vx = abs(self.ball.velocity.vx)
            self._apply_paddle_influence(self.left_paddle)
        if self.ball.collider.intersects(self.right_paddle.collider):
            self.ball.position.x = (
                self.right_paddle.position.x - self.ball.size.width
            )
            self.ball.velocity.vx = -abs(self.ball.velocity.vx)
            self._apply_paddle_influence(self.right_paddle)

        # Scoring – ball leaves left/right
        if self.ball.position.x < 0:
            self.right_score += 1
            logger.info(
                f"Right scores! {self.left_score} - {self.right_score}"
            )
            self._reset_ball(direction=1)
        if self.ball.position.x > self.size.width:
            self.left_score += 1
            logger.info(f"Left scores! {self.left_score} - {self.right_score}")
            self._reset_ball(direction=-1)

        if self.trail_enabled and hasattr(self, "ball"):
            self.trail.append((self.ball.position.x, self.ball.position.y))

    def draw(self, surface: Backend):  # type: ignore[override]
        """
        Draw the frame using the Backend as the 'surface'.
        """
        # We assume backend.begin_frame/end_frame is handled by Game.
        # Here we just draw the center line like in the original Pong.
        line_width = 5
        x = self.size.width // 2 - line_width // 2
        y = 0
        h = self.size.height
        surface.draw_rect(x, y, line_width, h, color=WHITE)

        # Scores near the top, left & right
        score_y = 20

        # Left score (slightly left of center)
        surface.draw_text(
            self.size.width // 4,
            score_y,
            str(self.left_score),
            color=WHITE,
        )

        # Right score (slightly right of center)
        surface.draw_text(
            self.size.width * 3 // 4,
            score_y,
            str(self.right_score),
            color=WHITE,
        )

        # Ghost trail on top of background, under ball (order up to you)
        if self.trail_enabled and self.trail:
            count = len(self.trail)
            for i, (x, y) in enumerate(self.trail):
                t = (i + 1) / count  # 0..1
                alpha = int(255 * t * 0.5)  # fade in, max 50% alpha
                # if your ball is e.g. 12x12 rect:
                size = 12
                surface.draw_rect(
                    int(x - size / 2),
                    int(y - size / 2),
                    size,
                    size,
                    (255, 255, 255, alpha),  # RGBA
                )

        self.draw_entities(surface)
        self.draw_overlays(surface)

    def _reset_ball(self, direction: int):
        """
        Reset ball to center, heading left (-1) or right (+1).
        """
        self.ball.position.x = self.size.width / 2 - self.ball.size.width / 2
        self.ball.position.y = self.size.height / 2 - self.ball.size.height / 2
        self.ball.velocity.vx = 250.0 * direction
        self.ball.velocity.vy = 200.0

    def _apply_paddle_influence(self, paddle: Paddle):
        """
        Adjust ball trajectory based on:
        - where it hit on the paddle (top/middle/bottom)
        - paddle vertical velocity (inertia)
        """
        # 1) Position-based angle
        ball_center = self.ball.position.y + self.ball.size.height / 2
        paddle_center = paddle.position.y + paddle.size.height / 2
        offset = (
            ball_center - paddle_center
        )  # >0 = lower half, <0 = upper half

        # normalize offset to [-1, 1]
        if paddle.size.height > 0:
            norm = offset / (paddle.size.height / 2)
        else:
            norm = 0.0
        norm = max(-1.0, min(1.0, norm))

        base_vy = 220.0  # base vertical speed from angle
        inertia_factor = 0.3  # how much paddle.vy affects ball.velocity.vy
        max_vy = 400.0  # safety clamp

        # angle component + inertia from paddle velocity
        new_vy = norm * base_vy + paddle.vy * inertia_factor

        # optional clamp so it doesn't go crazy fast
        if new_vy > max_vy:
            new_vy = max_vy
        elif new_vy < -max_vy:
            new_vy = -max_vy

        self.ball.velocity.vy = new_vy

        # (optional) tiny speed-up on each hit to make rallies more intense
        self.ball.velocity.vx *= 1.03

    def _photo_overlay(self, surface: Backend):
        """
        Overlay drawn on top of everything when photo_mode is enabled.
        Perfect for promo/devlog screenshots.
        """
        if not self.photo_mode:
            return

        title = "Deja Bounce"
        subtitle = "Finding the twist"
        extra = "in a Pong-like"

        # Simple positions for now – you can tune later.
        x = 20
        y = 60

        surface.draw_text(
            x,
            y,
            title,
            color=(155, 155, 255),
        )
        surface.draw_text(
            x,
            y + 30,
            subtitle,
            color=(155, 155, 255),
        )
        surface.draw_text(
            x,
            y + 60,
            extra,
            color=(155, 155, 255),
        )


def pong_scene_factory(game):
    """Pong scene factory."""
    return PongScene(game)


# pylint: enable=cyclic-import
