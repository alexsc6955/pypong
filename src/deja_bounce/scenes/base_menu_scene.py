"""
Base menu scene with common functionality for all menus.
"""

from __future__ import annotations

from mini_arcade_core import Event, EventType, Key, Scene
from mini_arcade_core.backend import Backend
from mini_arcade_core.ui.menu import Menu, MenuItem, MenuStyle

from deja_bounce.utils import logger


class BaseMenuScene(Scene):
    """
    Base class for menu scenes.

    :ivar menu (Menu): The menu instance.
    :ivar up_key (Key): Key to move selection up.
    :ivar down_key (Key): Key to move selection down.
    :ivar select_key (Key): Key to select menu item.
    """

    menu: Menu

    # Defaults (override per-scene if needed)
    up_key = Key.UP
    down_key = Key.DOWN
    select_key = Key.ENTER

    def menu_title(self) -> str | None:
        """
        Title of the menu. Override to provide a title.

        :return: The menu title, or None for no title.
        :rtype: str | None
        """
        return None

    def menu_style(self) -> MenuStyle:
        """
        Style of the menu. Override to provide custom styling.

        :return: The menu style.
        :rtype: MenuStyle
        """
        return MenuStyle()

    def menu_items(self) -> list[MenuItem]:
        """
        Menu items for this menu. Override to provide menu options.

        :return: List of menu items.
        :rtype: list[MenuItem]
        """
        raise NotImplementedError

    def on_escape(self):
        """What ESC does in this menu."""
        self.game.quit()

    def on_enter(self):
        self.menu = Menu(
            self.menu_items(),
            viewport=self.size,
            title=self.menu_title(),
            style=self.menu_style(),
        )

    def on_exit(self):
        logger.info("MenuScene on_exit")

    def handle_event(self, event: Event):  # type: ignore[override]
        if event.type == EventType.QUIT:
            self.game.quit()
            return

        if event.type == EventType.KEYDOWN and event.key == Key.ESCAPE:
            self.on_escape()
            return

        self.menu.handle_event(
            event,
            up_key=self.up_key,
            down_key=self.down_key,
            select_key=self.select_key,
        )

    def update(self, dt: float): ...

    def draw(self, surface: Backend):  # type: ignore[override]
        self.menu.draw(surface)
