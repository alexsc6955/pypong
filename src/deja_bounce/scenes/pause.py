"""
Pause scene for Deja Bounce game.
Provides a menu to continue or return to the main menu.
"""

from mini_arcade_core import Event, EventType, Key, Scene
from mini_arcade_core.backend import Backend
from mini_arcade_core.ui.menu import Menu, MenuItem

from deja_bounce.scenes.menu import MenuScene


class PauseScene(Scene):
    """Pause scene with options to continue or return to main menu."""

    menu: Menu

    def _pop_scene(self):
        self.game.pop_scene()

    def _change_to_main_menu(self):
        self.game.change_scene(MenuScene(self.game))

    def on_enter(self):
        """Initialize the pause menu."""
        self.menu = Menu(
            [
                MenuItem("Continue", self._pop_scene),
                MenuItem(
                    "Main Menu",
                    self._change_to_main_menu,
                ),
            ],
            x=60,
            y=80,
        )

    def on_exit(self): ...

    def handle_event(self, event: Event):
        if event.type == EventType.QUIT:
            self.game.quit()
            return

        self.menu.handle_event(
            event,
            up_key=Key.UP,
            down_key=Key.DOWN,
            select_key=Key.ENTER,
        )  # example keycodes
        if event.type == EventType.KEYDOWN and event.key == Key.ESCAPE:  # ESC
            self.game.pop_scene()

    def update(self, dt: float): ...  # pause menu logic only

    def draw(self, surface: Backend):
        x, y = 0, 0
        w, h = self.size.width, self.size.height

        surface.draw_rect(x, y, w, h, color=(0, 0, 0, 0.5))
        surface.draw_text(60, 40, "PAUSED")
        self.menu.draw(surface)
