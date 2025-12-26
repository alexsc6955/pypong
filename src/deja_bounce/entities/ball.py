"""
This module defines the Ball class.
"""

from __future__ import annotations

from mini_arcade_core.entity import KinematicEntity
from mini_arcade_core.spaces.d2 import KinematicData

from deja_bounce.utils import logger

from .common import RectDrawMixin


class Ball(RectDrawMixin, KinematicEntity):
    """
    Ball entity using KinematicEntity.
    """

    def __init__(self, data: KinematicData):
        super().__init__(data)
        logger.info("Ball created")
        self.base_vx = self.velocity.vx
        self.base_vy = self.velocity.vy
