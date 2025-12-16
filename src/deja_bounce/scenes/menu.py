"""
Minimal main menu scene for Deja Bounce.
"""

# Justification: These imports are necessary for scene management
# and may cause cyclic imports. They will be refactored later.
# pylint: disable=cyclic-import

# Justification: Duplicate code with PauseScene; acceptable for now.
# pylint: disable=duplicate-code
from __future__ import annotations

from mini_arcade_core import Backend, Event, EventType, Key, Scene
from mini_arcade_core.ui.menu import Menu, MenuItem, MenuStyle

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

    menu: Menu

    # --- Scene lifecycle -----------------------------------------------------

    def on_enter(self):
        logger.info("MenuScene on_enter")

        def start_game():
            self.game.change_scene("pong")

        def quit_game():
            self.game.quit()

        style = MenuStyle(
            background_color=(
                (*BACKGROUND, 1.0) if len(BACKGROUND) == 3 else BACKGROUND
            ),
            button_enabled=True,
            button_fill=BUTTON_FILL,
            button_border=BUTTON_BORDER,
            button_selected_border=HIGHLIGHT,
            normal=DIM,
            selected=WHITE,
            hint="Press ENTER to start · ESC to quit",
            hint_color=(200, 200, 200),
        )

        self.menu = Menu(
            [
                MenuItem("START", start_game),
                MenuItem("QUIT", quit_game),
            ],
            viewport=self.size,
            title="Deja Bounce",
            style=style,
        )

    def on_exit(self):
        logger.info("MenuScene on_exit")

    # --- Input ---------------------------------------------------------------

    def handle_event(self, event: Event):  # type: ignore[override]
        if event.type == EventType.QUIT:
            self.game.quit()
            return

        if event.type == EventType.KEYDOWN and event.key == Key.ESCAPE:
            self.game.quit()
            return

        self.menu.handle_event(
            event,
            up_key=Key.UP,
            down_key=Key.DOWN,
            select_key=Key.ENTER,
        )

    # --- Update / Draw -------------------------------------------------------

    def update(self, dt: float): ...

    def draw(self, surface: Backend):  # type: ignore[override]
        self.menu.draw(surface)


def menu_scene_factory(game):
    """Menu scene factory."""
    return MenuScene(game)


# pylint: enable=cyclic-import,duplicate-code
