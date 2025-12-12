"""
Minimal main menu scene for Deja Bounce.
"""

# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import
from __future__ import annotations

from mini_arcade_core import Backend, Event, EventType, Game, Scene

from deja_bounce.constants import (
    BACKGROUND,
    BUTTON_BORDER,
    BUTTON_FILL,
    DIM,
    HIGHLIGHT,
    WHITE,
)
from deja_bounce.utils import logger


class MenuScene(Scene):
    """
    Simple main menu scene for Deja Bounce.

    Options:
      [0] Start Game
      [1] Quit
    """

    def __init__(self, game: Game):
        super().__init__(game)
        self.selected_index = 0  # 0 = Start, 1 = Quit

        self.add_overlay(self._title_overlay)
        self.add_overlay(self._hint_overlay)

    # --- Scene lifecycle -----------------------------------------------------

    def on_enter(self) -> None:
        logger.info("MenuScene on_enter")

    def on_exit(self) -> None:
        logger.info("MenuScene on_exit")

    # --- Input ---------------------------------------------------------------

    def handle_event(self, event: Event) -> None:  # type: ignore[override]
        # Justification: Importing here to avoid cyclic import issues.
        # pylint: disable=import-outside-toplevel
        from .pong import PongScene

        # pylint: enable=import-outside-toplevel

        if event.type == EventType.QUIT:
            logger.info("Menu: Quit event received")
            self.game.quit()
            return

        if event.type != EventType.KEYDOWN:
            return

        key = event.key
        logger.debug(f"Menu key down: {key}")

        # ESC quits from menu
        if key == 27:
            logger.info("Menu: ESC pressed, quitting game")
            self.game.quit()
            return

        # Up (W or arrow up) -> previous option
        if key in (ord("w"), 1073741906):  # SDL_K_UP
            self.selected_index = (self.selected_index - 1) % 2
            logger.info(f"Menu: selected_index={self.selected_index}")
            return

        # Down (S or arrow down) -> next option
        if key in (ord("s"), 1073741905):  # SDL_K_DOWN
            self.selected_index = (self.selected_index + 1) % 2
            logger.info(f"Menu: selected_index={self.selected_index}")
            return

        # Enter or Space -> confirm
        if key in (13, 32):  # Enter or Space
            if self.selected_index == 0:
                logger.info("Menu: Start Game selected")
                # Switch to PongScene
                self.game.change_scene(PongScene(self.game))
            else:
                logger.info("Menu: Quit selected")
                self.game.quit()

    # --- Update / Draw -------------------------------------------------------

    def update(self, dt: float) -> None:  # type: ignore[override]
        # No animation yet, but you can add menu effects later.
        self.game.backend.set_clear_color(*BACKGROUND)  # type: ignore[attr-defined]

    def draw(self, surface: Backend) -> None:  # type: ignore[override]
        """
        Render a very simple menu using rectangles as buttons.
        No text support in backend yet, so we rely on shapes.
        """
        option_w = self.size.width // 3
        option_h = 40
        x = self.size.width // 2 - option_w // 2
        gap = 20

        start_y = self.size.height // 2 - option_h - gap // 2
        quit_y = self.size.height // 2 + gap // 2

        # Title
        surface.draw_text(
            self.size.width // 2 - 100,
            self.size.height // 3 - 40,
            "DEJA BOUNCE",
            color=WHITE,
        )

        # Helper: draw one button
        def draw_button(y: int, label: str, selected: bool) -> None:
            # Outer border / highlight
            border_color = HIGHLIGHT if selected else BUTTON_BORDER
            surface.draw_rect(
                x - 4,
                y - 4,
                option_w + 8,
                option_h + 8,
                color=border_color,
            )

            # Inner fill
            surface.draw_rect(x, y, option_w, option_h, color=BUTTON_FILL)

            # Text
            text_color = WHITE if selected else DIM
            surface.draw_text(x + 20, y + 10, label, color=text_color)

        draw_button(start_y, "START", selected=self.selected_index == 0)
        draw_button(quit_y, "QUIT", selected=self.selected_index == 1)

    def _title_overlay(self, surface: Backend) -> None:
        surface.draw_text(
            self.size.width // 2 - 80,
            80,
            "Deja Bounce",
            color=WHITE,
        )

    def _hint_overlay(self, surface: Backend) -> None:
        surface.draw_text(
            self.size.width // 2 - 120,
            130,
            "Press ENTER to start · ESC to quit",
            color=(200, 200, 200),
        )


# pylint: enable=cyclic-import
