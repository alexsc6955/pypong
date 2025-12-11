"""
This module defines the Ball class.
"""

from __future__ import annotations

from mini_arcade_core import Backend, KinematicData, KinematicEntity

from deja_bounce.utils import logger


class Ball(KinematicEntity):
    """
    Ball entity using KinematicEntity.
    """

    def __init__(self, data: KinematicData):
        super().__init__(data)

        logger.info("Ball created")

    def draw(self, surface: Backend) -> None:
        surface.draw_rect(
            int(self.position.x),
            int(self.position.y),
            self.size.width,
            self.size.height,
        )
