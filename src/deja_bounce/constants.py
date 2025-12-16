"""
Constants for the game.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _find_assets_root() -> Path:
    """Return the path to the `assets` directory.

    Works in:
    - dev: repo/assets (when running from source tree)
    - pip install: site-packages/assets
    - PyInstaller onefile: _MEIPASS/assets (if bundled with --add-data)
    """
    # 1) PyInstaller onefile support
    # Justification: This is the documented way to access _MEIPASS
    # pylint: disable=protected-access
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
        candidate = base / "assets"
        if candidate.is_dir():
            return candidate
    # pylint: enable=protected-access

    # 2) Dev / pip-installed: walk upwards and look for an `assets` folder
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "assets"
        if candidate.is_dir():
            return candidate

    # 3) Last-resort fallback (we can raise instead if you prefer)
    raise FileNotFoundError("Could not locate 'assets' directory.")


ASSETS_ROOT = _find_assets_root()
ROOT = ASSETS_ROOT.parent

FPS = 60
WINDOW_SIZE = (700, 500)
PADDLE_SIZE = (10, 100)

# Colors
BACKGROUND = (5, 5, 15)
WHITE = (240, 240, 240)
DIM = (120, 120, 140)

# Button colors
BUTTON_FILL = (20, 20, 40)
BUTTON_BORDER = (70, 70, 120)
HIGHLIGHT = (140, 200, 255)
