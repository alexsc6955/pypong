"""
Minimal main menu scene for Deja Bounce.
"""

from __future__ import annotations

from mini_arcade_core import register_scene
from mini_arcade_core.ui.menu import MenuItem, MenuStyle

from deja_bounce.constants import (
    BACKGROUND,
    BUTTON_BORDER,
    BUTTON_FILL,
    DIM,
    HIGHLIGHT,
    WHITE,
)
from deja_bounce.difficulty import DIFFICULTY_PRESETS
from deja_bounce.scenes.base_menu_scene import BaseMenuScene
from deja_bounce.utils import logger


@register_scene("menu")
class MenuScene(BaseMenuScene):
    """
    Simple main menu scene for Deja Bounce.

    Options:
      [0] Start Game
      [1] Quit
      [2] Cycle Difficulty
    """

    def menu_title(self) -> str | None:
        return "Deja Bounce"

    def menu_style(self) -> MenuStyle:
        return MenuStyle(
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

    def menu_items(self):
        logger.info("MenuScene on_enter")

        levels = list(DIFFICULTY_PRESETS.keys())

        def cycle_difficulty():
            cur = self.game.settings.difficulty
            idx = levels.index(cur) if cur in levels else 0
            new = levels[(idx + 1) % len(levels)]
            self.game.settings.difficulty = new

            # update the label live
            self.menu.items[2] = MenuItem(
                f"DIFFICULTY: {new.upper()}", cycle_difficulty
            )

        def start_game():
            self.game.change_scene("pong")

        def quit_game():
            self.game.quit()

        items = [
            MenuItem("START", start_game),
            MenuItem("QUIT", quit_game),
            MenuItem(
                f"DIFFICULTY: {self.game.settings.difficulty.upper()}",
                cycle_difficulty,
            ),
        ]

        return items
