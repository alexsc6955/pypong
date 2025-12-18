"""
Difficulty presets for CPU-controlled paddles.

:cvar DIFFICULTY_PRESETS (dict[str, CpuConfig]):
    A dictionary mapping difficulty levels to CpuConfig instances.
"""

from deja_bounce.controllers import CpuConfig

DIFFICULTY_PRESETS: dict[str, CpuConfig] = {
    "easy": CpuConfig(
        max_speed=180.0,
        dead_zone=18.0,
        reaction_distance=140.0,
        error_margin=40.0,
    ),
    "normal": CpuConfig(
        max_speed=240.0,
        dead_zone=10.0,
        reaction_distance=170.0,
        error_margin=28.0,
    ),
    "hard": CpuConfig(
        max_speed=300.0,
        dead_zone=6.0,
        reaction_distance=220.0,
        error_margin=16.0,
    ),
    "insane": CpuConfig(
        max_speed=380.0,
        dead_zone=3.0,
        reaction_distance=9999.0,
        error_margin=4.0,
    ),
}
