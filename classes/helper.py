"""
'helper.py' module.
Contains helper functions
"""
from pymunk import Vec2d


def flipy(p, h):
    """Convert chipmunk coordinates to Pygame coordinates."""
    return Vec2d(p[0], -p[1] + h)