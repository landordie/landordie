"""
'helper.py' module.
Contains helper functions
"""
from pymunk.vec2d import Vec2d


def flipy(p, h):
    """
    Convert chipmunk coordinates to Pygame coordinates.
    :param p: coordinate point tuple
    :param h: height of the current scene (window)
    :return:
    """
    return Vec2d(p[0], -p[1] + h)


def draw_text(display, message, position, font, color=(0, 0, 0)):
    """
    Draw text on the given screen surface
    :param display: screen
    :param message: text message to draw
    :param position: position of the text message
    :param font: font of text message
    :param color: color of text message
    """
    text = font.render(message, False, color)
    text_rect = text.get_rect(center=position)
    display.blit(text, text_rect)
