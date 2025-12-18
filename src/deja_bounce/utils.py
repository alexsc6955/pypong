"""
DejaBounce utils
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def find_assets_root() -> Path:
    """Return the path to the `assets` directory.

    Works in:
    - dev: repo/assets (when running from source tree)
    - pip install: site-packages/assets
    - PyInstaller onefile: _MEIPASS/assets (if bundled with --add-data)

    :return: Path to the assets directory.
    :rtype: Path

    :raises FileNotFoundError: If the assets directory cannot be found.
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


def _classname_from_locals(locals_: dict) -> Optional[str]:
    self_obj = locals_.get("self")
    if self_obj is not None:
        return type(self_obj).__name__
    cls_obj = locals_.get("cls")
    if isinstance(cls_obj, type):
        return cls_obj.__name__
    return None


class EnsureClassName(logging.Filter):
    """
    Populate record.classname by finding the *emitting* frame:
    we match by (pathname, funcName) and read self/cls from its locals.
    Falls back to "-" when not in a class context (module funcs/staticmethods).
    """

    def filter(self, record: logging.LogRecord) -> bool:
        # keep any explicitly-provided classname
        if getattr(record, "classname", None):
            return True

        target_path = record.pathname  # absolute path to the file
        target_func = record.funcName  # function name that logged

        # Walk current stack; stop when we match the record’s file+func.
        # Justification: Accessing protected member for logging purposes.
        # pylint: disable=protected-access
        f = sys._getframe()
        # pylint: enable=protected-access
        for _ in range(200):  # safety cap
            if f is None:
                break
            code = f.f_code
            if code.co_filename == target_path and code.co_name == target_func:
                clsname = _classname_from_locals(f.f_locals)
                record.classname = clsname or "-"
                return True
            f = f.f_back

        # Fallback: we didn’t find the exact frame (wrappers, C calls, etc.)
        record.classname = "-"
        return True


class ConsoleColorFormatter(logging.Formatter):
    """
    A custom console formatter for the logger.

    This formatter allows log messages to be formatted with ANSI escape codes for colors
    based on the log level.
    """

    COLORS = {
        logging.ERROR: "\033[91m",  # Red
        logging.DEBUG: "\033[96m",  # Cyan
        logging.INFO: "\033[97m",  # White
        logging.WARNING: "\033[93m",  # Yellow
        logging.CRITICAL: "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def __init__(self, fmt=None, datefmt=None, style="%"):
        """
        :param fmt: The format string for the log message.
        :type fmt: str, optional

        :param datefmt: The format string for the date.
        :type datefmt: str, optional

        :param style: The style for the format string.
        :type style: str, optional
        """
        super().__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record with ANSI escape codes.

        This method formats the log record using ANSI escape codes for colors
        based on the log level.

        :param record: The log record to be formatted.
        :type record: logging.LogRecord

        :return: The formatted log message as a string with ANSI escape codes.
        :rtype: str
        """

        color = ConsoleColorFormatter.COLORS.get(
            record.levelno, ConsoleColorFormatter.COLORS["RESET"]
        )
        formatted_record = super().format(record)
        return (
            f"{color}{formatted_record}{ConsoleColorFormatter.COLORS['RESET']}"
        )


LOGGER_FORMAT = (
    "%(asctime)s [%(levelname)-8.8s] [%(name)s] "
    "%(module)s.%(classname)s.%(funcName)s: "
    "%(message)s (%(filename)s:%(lineno)d)"
)
logging.basicConfig(level=logging.DEBUG, format=LOGGER_FORMAT)
logger = logging.getLogger("deja-bounce")
logger.addFilter(EnsureClassName())
console_handler = logging.StreamHandler()
console_handler.setFormatter(ConsoleColorFormatter(LOGGER_FORMAT))
logger.addHandler(console_handler)
