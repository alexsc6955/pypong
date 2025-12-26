"""
Minimal Pong-like scene using mini-arcade-core.
"""

# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import

from __future__ import annotations

from typing import TYPE_CHECKING

from mini_arcade_core.backend import Backend
from mini_arcade_core.keymaps import Key
from mini_arcade_core.managers.cheats import CheatSystem
from mini_arcade_core.scenes import BaseSceneSystem
from mini_arcade_core.spaces.d2 import Bounds2D, Size2D, VerticalBounce

from deja_bounce.controllers.cpu import CpuPaddleController
from deja_bounce.difficulty import DIFFICULTY_PRESETS
from deja_bounce.entities.paddle import Paddle

from .commands import (
    CpuVsCpuCommand,
    GodModeCommand,
    MovePaddleCommand,
    ResetRallyCommand,
    ScoreLeftCommand,
    ScoreRightCommand,
    SetWinnerP1Command,
    SetWinnerP2Command,
    SlowMoCommand,
    StopPaddleCommand,
)

if TYPE_CHECKING:
    from deja_bounce.scenes.pong import PongScene


class PaddleControlSystem(BaseSceneSystem):
    """
    System to handle paddle controls.
    """

    priority = 50
    enabled = True
    scene: PongScene

    def on_enter(self) -> None:
        self.scene.services.input.on_key_down(
            Key.W, MovePaddleCommand(self.scene.left_paddle, "up"), "p1_up"
        )
        self.scene.services.input.on_key_down(
            Key.S, MovePaddleCommand(self.scene.left_paddle, "down"), "p1_down"
        )
        self.scene.services.input.on_key_up(
            Key.W, StopPaddleCommand(self.scene.left_paddle, "up"), "p1_up"
        )
        self.scene.services.input.on_key_up(
            Key.S, StopPaddleCommand(self.scene.left_paddle, "down"), "p1_down"
        )


class BallWallBounceSystem(BaseSceneSystem):
    """
    System to handle ball bouncing off walls.
    """

    priority = 60
    enabled = True
    scene: PongScene

    def __init__(self, scene):
        super().__init__(scene)
        wall_height = scene.model.wall_height
        self.bounds = Bounds2D.from_size(
            Size2D(scene.size.width - 0, scene.size.height - 2 * wall_height)
        )
        self.ball_vertical_bounds = VerticalBounce(self.bounds)

    def update(self, dt: float) -> None:
        if self.scene.model.wall_left:
            self.bounds.left = self.scene.model.wall_height
        else:
            self.bounds.left = 0.0
        if self.scene.model.wall_right:
            self.bounds.right = (
                self.scene.size.width - self.scene.model.wall_height
            )
        else:
            self.bounds.right = float(self.scene.size.width)
        self.ball_vertical_bounds.apply(self.scene.ball)


class BallPaddleCollisionSystem(BaseSceneSystem):
    """
    System to handle ball collisions with paddles.
    """

    priority = 70
    enabled = True
    scene: PongScene

    def _apply_paddle_influence(self, paddle: Paddle):
        """
        Adjust ball trajectory based on:
        - where it hit on the paddle (top/middle/bottom)
        - paddle vertical velocity (inertia)
        """
        scene: PongScene = self.scene
        # 1) Position-based angle
        ball_center = scene.ball.position.y + scene.ball.size.height / 2
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

        scene.ball.velocity.vy = new_vy

        # (optional) tiny speed-up on each hit to make rallies more intense
        scene.ball.velocity.vx *= 1.03

    def update(self, dt: float) -> None:
        # Paddle collisions
        if self.scene.ball.collider.intersects(
            self.scene.left_paddle.collider
        ):
            self.scene.ball.position.x = (
                self.scene.left_paddle.position.x
                + self.scene.left_paddle.size.width
            )
            self.scene.ball.velocity.vx = abs(self.scene.ball.velocity.vx)
            self._apply_paddle_influence(self.scene.left_paddle)

        if self.scene.ball.collider.intersects(
            self.scene.right_paddle.collider
        ):
            self.scene.ball.position.x = (
                self.scene.right_paddle.position.x - self.scene.ball.size.width
            )
            self.scene.ball.velocity.vx = -abs(self.scene.ball.velocity.vx)
            self._apply_paddle_influence(self.scene.right_paddle)


class CpuPaddleControlSystem(BaseSceneSystem):
    """
    System to control the CPU paddle.

    :ivar priority (int): The priority of the system.
    :ivar enabled (bool): Whether the system is enabled.
    :ivar scene (PongScene): The PongScene instance.
    """

    priority = 80
    enabled = True
    scene: PongScene

    def __init__(self, scene: PongScene):
        super().__init__(scene)
        level = scene.game.settings.difficulty
        cpu_cfg = DIFFICULTY_PRESETS.get(level, DIFFICULTY_PRESETS["normal"])
        self.controller = CpuPaddleController(
            scene.right_paddle, scene.ball, side="RIGHT", config=cpu_cfg
        )

    def update(self, dt: float) -> None:
        self.controller.update(dt)


class ResetRallySystem(BaseSceneSystem):
    """
    System to reset the rally after a score.
    """

    priority = 95
    enabled = True

    def update(self, dt: float) -> None:
        if not self.scene.model.reset_rally:
            return

        self.scene.ball.position.x = (
            self.scene.size.width / 2 - self.scene.ball.size.width / 2
        )
        self.scene.ball.position.y = (
            self.scene.size.height / 2 - self.scene.ball.size.height / 2
        )
        self.scene.ball.velocity.vx = 250.0 * float(
            self.scene.model.reset_rally_direction
        )
        self.scene.ball.velocity.vy = 200.0
        ResetRallyCommand().execute(self.scene.model)


class BallOutSystem(BaseSceneSystem):
    """
    System to detect when the ball goes out of bounds and award score.
    """

    priority = 100  # run late in update
    enabled = True

    def update(self, dt: float) -> None:
        missed_side = None
        if self.scene.ball.position.x < 0:
            missed_side = "LEFT"
        elif self.scene.ball.position.x > self.scene.size.width:
            missed_side = "RIGHT"
        if missed_side is None:
            return

        if missed_side == "LEFT":
            ScoreRightCommand().execute(self.scene.model)
        else:
            ScoreLeftCommand().execute(self.scene.model)


class PongCheatsSystem(CheatSystem["PongScene"]):
    """
    Cheat system for PongScene.
    """

    priority = 200

    def on_enter(self):
        self.register("god_mode", ["G", "O", "D"], GodModeCommand("P1"))
        self.register("slow_mo", ["S", "L", "O", "W"], SlowMoCommand())
        self.register(
            "cpu_vs_cpu",
            ["C", "P", "U"],
            CpuVsCpuCommand(),
        )


class GodModeSystem(BaseSceneSystem):
    """
    System to handle god mode for players.
    """

    priority = 90
    enabled = True

    def update(self, dt: float) -> None:
        if self.scene.model.god_mode_p1:
            self.scene.model.wall_left = True
            # Keep ball on screen for player 1
            if self.scene.ball.position.x < 0:
                self.scene.ball.position.x = 0
                self.scene.ball.velocity.vx = abs(self.scene.ball.velocity.vx)
        else:
            self.scene.model.wall_left = False

        if self.scene.model.god_mode_p2:
            self.scene.model.wall_right = True
            # Keep ball on screen for player 2
            if self.scene.ball.position.x > self.scene.size.width:
                self.scene.ball.position.x = (
                    self.scene.size.width - self.scene.ball.size.width
                )
                self.scene.ball.velocity.vx = -abs(self.scene.ball.velocity.vx)
        else:
            self.scene.model.wall_right = False


class SlowMoSystem(BaseSceneSystem):
    """
    System to handle slow motion mode.
    """

    priority = 85  # after collisions can change velocity, before entity update next frame
    enabled = True

    def update(self, dt: float) -> None:
        factor = 0.25 if self.scene.model.slow_mo else 1.0
        self.scene.ball.time_scale = factor
        self.scene.right_paddle.time_scale = factor


class CPUVsCPUSystem(BaseSceneSystem):
    """
    System to handle CPU vs CPU mode.
    """

    priority = 45  # before PaddleControlSystem
    enabled = True

    def update(self, dt: float) -> None:
        if self.scene.model.cpu_vs_cpu:
            # Control left paddle with CPU as well
            level = self.scene.game.settings.difficulty
            cpu_cfg = DIFFICULTY_PRESETS.get(
                level, DIFFICULTY_PRESETS["normal"]
            )
            controller = CpuPaddleController(
                self.scene.left_paddle,
                self.scene.ball,
                side="LEFT",
                config=cpu_cfg,
            )
            controller.update(dt)


class TrailModeSystem(BaseSceneSystem):
    """
    System to handle trail mode.
    """

    priority = 98
    enabled = True
    scene: PongScene

    def update(self, dt: float) -> None:
        if self.scene.model.trail_mode:
            self.scene.model.trail.append(
                (self.scene.ball.position.x, self.scene.ball.position.y)
            )

    def draw(self, surface: Backend) -> None:
        if self.scene.model.trail_mode:
            count = len(self.scene.model.trail)
            for i, (x, y) in enumerate(self.scene.model.trail):
                t = (i + 1) / count  # 0..1
                alpha = t * 0.5  # fade in, max 50% alpha
                # if your ball is e.g. 12x12 rect:
                size = 12
                surface.draw_rect(
                    int(x - size / 2),
                    int(y - size / 2),
                    size,
                    size,
                    (255, 255, 255, alpha),  # RGBA
                )


class WinConditionSystem(BaseSceneSystem):
    """
    System to check for win conditions.
    """

    priority = 110  # after scoring

    def update(self, dt: float) -> None:
        model = self.scene.model
        winning_score = model.winning_score
        if model.score.left >= winning_score:
            SetWinnerP1Command().execute(model)
        elif model.score.right >= winning_score:
            SetWinnerP2Command().execute(model)
