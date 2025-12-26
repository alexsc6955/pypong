"""
Minimal Pong-like scene using mini-arcade-core.
"""

from __future__ import annotations

from mini_arcade_core import Game
from mini_arcade_core.backend import Backend, Event
from mini_arcade_core.keymaps import Key
from mini_arcade_core.scenes import Scene, register_scene
from mini_arcade_core.spaces.d2 import KinematicData, Position2D, Size2D

from deja_bounce.constants import PADDLE_SIZE
from deja_bounce.entities import Ball, Paddle, PaddleConfig
from deja_bounce.utils import logger

from .commands import (
    EnableTrialModeCommand,
    PauseGameCommand,
    PhotoModeCommand,
    QuitCommand,
    TakeScreenshotCommand,
)
from .models import PongModel, ScoreState
from .overlays import PhotoOverlay, ScoreOverlay, WallsOverlay
from .systems import (
    BallOutSystem,
    BallPaddleCollisionSystem,
    BallWallBounceSystem,
    CpuPaddleControlSystem,
    CPUVsCPUSystem,
    GodModeSystem,
    PaddleControlSystem,
    PongCheatsSystem,
    ResetRallySystem,
    SlowMoSystem,
    TrailModeSystem,
    WinConditionSystem,
)


# pylint: disable=too-many-instance-attributes
@register_scene("pong")
class PongScene(Scene):
    """
    Minimal scene: opens a window, clears screen, handles quit/ESC.
    """

    right_paddle: Paddle
    left_paddle: Paddle
    ball: Ball

    def __init__(self, game: Game):
        """
        :param game: The game instance.
        :type game: Game
        """
        super().__init__(game)
        self.model = PongModel(
            score=ScoreState(),
        )
        self._set_entities()

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
                vx=-250.0,
                vy=-200.0,
            )
        )

    def on_enter(self):
        logger.info("PongScene on_enter")
        self.services.input.on_quit(QuitCommand(), "quit")
        self.services.input.on_key_down(
            Key.T, EnableTrialModeCommand(), "trial_mode"
        )
        self.services.input.on_key_down(
            Key.ESCAPE, PauseGameCommand(), "pause_game"
        )
        self.services.input.on_key_down(
            Key.P, PhotoModeCommand(), "photo_mode"
        )
        self.services.input.on_key_down(
            Key.F12, TakeScreenshotCommand(), "screenshot"
        )
        self.services.entities.add(
            self.left_paddle, self.right_paddle, self.ball
        )
        self.services.overlays.add(PhotoOverlay(self.model))
        self.services.overlays.add(WallsOverlay(self.model, self.size))
        self.services.overlays.add(ScoreOverlay(self.model, self.size))
        self.services.systems.add(PaddleControlSystem(self))
        self.services.systems.add(CpuPaddleControlSystem(self))
        self.services.systems.add(BallWallBounceSystem(self))
        self.services.systems.add(BallPaddleCollisionSystem(self))
        self.services.systems.add(ResetRallySystem(self))
        self.services.systems.add(BallOutSystem(self))
        self.services.systems.add(PongCheatsSystem(scene=self))
        self.services.systems.add(GodModeSystem(self))
        self.services.systems.add(SlowMoSystem(self))
        self.services.systems.add(CPUVsCPUSystem(self))
        self.services.systems.add(TrailModeSystem(self))
        self.services.systems.add(WinConditionSystem(self))
        self._systems_on_enter()

    def on_exit(self):
        logger.info("PongScene on_exit")

    def handle_event(self, event: Event):  # type: ignore[override]
        """
        Handle backend events (mini_arcade_core.Event).
        """
        if self._systems_handle_event(event):
            return
        self.services.input.handle_event(event, self)

    def update(self, dt: float):
        """
        Update game logic. (None yet.)
        """
        self.services.entities.update(dt)
        self._systems_update(dt)

    def draw(self, surface: Backend):  # type: ignore[override]
        """
        Draw the frame using the Backend as the 'surface'.
        """
        self.services.entities.draw(surface)
        self._systems_draw(surface)
        self.services.overlays.draw(surface)
