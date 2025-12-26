"""
Data models for the Pong scene.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Literal, Optional

from mini_arcade_core.scenes import SceneModel

Player = Literal["P1", "P2"]


@dataclass
class ScoreState:
    """
    Score state for the Pong scene.

    :ivar left (int): Score for the left player.
    :ivar right (int): Score for the right player.
    """

    left: int = 0
    right: int = 0


# Justification: The model has many attributes to represent game state.
# pylint: disable=too-many-instance-attributes
@dataclass
class PongModel(SceneModel):
    """
    Data model for the Pong scene.

    :ivar wall_height (int): Height of the walls.
    :ivar wall_left (bool): Whether the left wall is present.
    :ivar wall_right (bool): Whether the right wall is present.
    :ivar score (Optional[ScoreState]): Current score state.
    :ivar reset_rally (bool): Whether to reset the rally.
    :ivar reset_rally_direction (Optional[int]): Direction to serve after reset
        (-1 for left, +1 for right).
    :ivar god_mode_p1 (bool): God mode for player 1.
    :ivar god_mode_p2 (bool): God mode for player 2.
    :ivar slow_mo (bool): Whether slow motion is enabled.
    :ivar cpu_vs_cpu (bool): Whether CPU vs CPU mode is enabled.
    :ivar trail_mode (bool): Whether trail mode is enabled.
    :ivar trail (deque): Trail of previous ball positions.
    :ivar photo_mode (bool): Whether photo mode is enabled.
    """

    # walls
    wall_height: int = 5
    wall_left: bool = False
    wall_right: bool = False

    # match
    score: Optional[ScoreState] = None
    reset_rally: bool = False
    reset_rally_direction: Optional[int] = None  # -1 for left, +1 for right
    winning_score: int = 10
    winner: Optional[Player] = None

    # toggles / debug
    god_mode_p1: bool = False
    god_mode_p2: bool = False
    slow_mo: bool = False
    cpu_vs_cpu: bool = False
    trail_mode: bool = False
    trail: deque = deque(maxlen=15)
    photo_mode: bool = False


# pylint: enable=too-many-instance-attributes
