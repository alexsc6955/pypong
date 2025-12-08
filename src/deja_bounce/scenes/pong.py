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
    Event,
    EventType,
    Game,
    Scene,
    SpriteEntity,
)

from deja_bounce.constants import PADDLE_SIZE, ROOT, WHITE
from deja_bounce.controllers import CpuConfig, CpuPaddleController
from deja_bounce.entities import Ball, Paddle
from deja_bounce.utils import logger


# pylint: disable=too-many-instance-attributes
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

        self.trail_enabled = False
        self.trail = deque(maxlen=15)

        self.photo_mode = False
        self.add_overlay(self._photo_overlay)

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

            if event.key == ord("t"):
                self.trail_enabled = not self.trail_enabled

            if event.key == ord("p"):
                # toggle photo mode; ensure trail on when enabled
                self.photo_mode = not self.photo_mode
                if self.photo_mode:
                    self.trail_enabled = True

            if event.key == 1073741893:  # F12
                self.game.screenshot(
                    "screenshot.bmp", str(ROOT / "screenshots")
                )
                logger.info("Screenshot saved: screenshot.bmp")
                return

            if event.key == 27:  # ESC
                # Justification: Importing here to avoid cyclic import issues.
                # pylint: disable=import-outside-toplevel
                from deja_bounce.scenes.menu import MenuScene

                # pylint: enable=import-outside-toplevel

                self.game.change_scene(MenuScene(self.game))
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
            # snap ball outside the paddle so we don't keep intersecting
            self.ball.x = self.left.x + self.left.width

            # ensure it goes to the right
            self.ball.vx = abs(self.ball.vx)

            # apply angle + inertia
            self._apply_paddle_influence(self.left)

        if self._intersects(self.ball, self.right):
            self.ball.x = self.right.x - self.ball.width

            # ensure it goes to the left
            self.ball.vx = -abs(self.ball.vx)

            self._apply_paddle_influence(self.right)

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

        if self.trail_enabled and hasattr(self, "ball"):
            self.trail.append((self.ball.x, self.ball.y))

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
        surface.draw_rect(x, y, line_width, h, color=WHITE)

        # Scores near the top, left & right
        score_y = 20

        # Left score (slightly left of center)
        surface.draw_text(
            self.width // 4,
            score_y,
            str(self.left_score),
            color=WHITE,
        )

        # Right score (slightly right of center)
        surface.draw_text(
            self.width * 3 // 4,
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

        # Draw all entities
        for ent in self.entities:
            ent.draw(surface)

        self.draw_overlays(surface)

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

    def _apply_paddle_influence(self, paddle: Paddle) -> None:
        """
        Adjust ball trajectory based on:
        - where it hit on the paddle (top/middle/bottom)
        - paddle vertical velocity (inertia)
        """
        # 1) Position-based angle
        ball_center = self.ball.y + self.ball.height / 2
        paddle_center = paddle.y + paddle.height / 2
        offset = (
            ball_center - paddle_center
        )  # >0 = lower half, <0 = upper half

        # normalize offset to [-1, 1]
        if paddle.height > 0:
            norm = offset / (paddle.height / 2)
        else:
            norm = 0.0
        norm = max(-1.0, min(1.0, norm))

        base_vy = 220.0  # base vertical speed from angle
        inertia_factor = 0.3  # how much paddle.vy affects ball.vy
        max_vy = 400.0  # safety clamp

        # angle component + inertia from paddle velocity
        new_vy = norm * base_vy + paddle.vy * inertia_factor

        # optional clamp so it doesn't go crazy fast
        if new_vy > max_vy:
            new_vy = max_vy
        elif new_vy < -max_vy:
            new_vy = -max_vy

        self.ball.vy = new_vy

        # (optional) tiny speed-up on each hit to make rallies more intense
        self.ball.vx *= 1.03

    def _photo_overlay(self, surface: Backend) -> None:
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


# pylint: enable=cyclic-import
