"""
Pause scene for Deja Bounce game.
Provides a menu to continue or return to the main menu.
"""

from __future__ import annotations

from mini_arcade_core import register_scene
from mini_arcade_core.ui.menu import MenuItem, MenuStyle

from deja_bounce.scenes.base_menu_scene import BaseMenuScene


@register_scene("pause")
class PauseScene(BaseMenuScene):
    """
    Pause scene with options to continue or return to main menu.
    """

    def menu_title(self) -> str | None:
        return "PAUSED"

    def menu_style(self) -> MenuStyle:
        return MenuStyle(
            overlay_color=(0, 0, 0, 0.5),
            panel_color=(20, 20, 20, 0.75),
        )

    def _pop_scene(self):
        self.game.pop_scene()

    def _change_to_main_menu(self):
        self.game.change_scene("menu")

    def menu_items(self):
        """Initialize the pause menu."""
        return [
            MenuItem("Continue", self._pop_scene),
            MenuItem(
                "Main Menu",
                self._change_to_main_menu,
            ),
        ]
