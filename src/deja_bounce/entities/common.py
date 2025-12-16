"""
Common entity mixins.
"""

from __future__ import annotations

from mini_arcade_core import Backend, Position2D, Size2D


class RectDrawMixin:
    """
    Mixin that provides a default rect-based draw() implementation.

    Expects:
    - self.position.x / self.position.y (floats)
    - self.size.width / self.size.height (ints)

    :ivar position (Position2D): Position of the entity.
    :ivar size (Size2D): Size of the entity.
    """

    position: Position2D
    size: Size2D

    def draw(self, surface: Backend):
        """
        Default rect-based draw implementation.

        :param surface: Backend surface to draw on.
        :type surface: Backend
        """
        surface.draw_rect(
            int(self.position.x),
            int(self.position.y),
            self.size.width,
            self.size.height,
        )
