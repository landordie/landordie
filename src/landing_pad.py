"""
'landing_pad.py' module.
Used in initializing the landing pad Sprite object.
"""
from .constants import pg
from pymunk import Segment
from random import randint
from .sprite_class import Sprite
from .helper import flipy


class LandingPad(Sprite):
    """LandingPad instance class implementation."""

    def __init__(self, width, height):
        """Virtually private constructor which initializes the game landing pad Sprite."""
        # Call the super class (Sprite) initialization method.
        # Ensures that this class inherits its behaviour from its Superclass.
        super().__init__('assets/frames/landing_pad.png')

        # Adjust landing pad image rectangle
        self.rect.top = randint(height // 1.7, height // 1.5)
        self.rect.right = randint(155, width - 100)

        self.mask = pg.mask.from_surface(self.image)

    def pymunk_pad(self, space, height):
        """
        Generate a Pymunk segment object which is used to detect
        physics based collision between the spacecraft and the landing pad.
        (collision tracking based on Pymunk physics objects)
        :param space: Pymunk physics space
        :param height: current scene (window) height
        :return: Pymunk segment object
        """
        pm_pad = Segment(space.static_body, flipy((self.rect.left + 14, self.rect.top + 16), height),
                         flipy((self.rect.right - 14, self.rect.top + 16), height), 5)
        pm_pad.collision_type = 4
        return pm_pad

    def check_for_landing_attempt(self, spacecraft):
        """
        Check for successful landing attempt.
        :param spacecraft: Spacecraft instance object
        :return: boolean (True if all conditions are met)
        """
        # If the spacecraft is inside the boundaries of the landing pad with proper velocity
        if spacecraft.rect.right < self.rect.right and spacecraft.rect.left > self.rect.left \
                and spacecraft.rect.bottom <= self.rect.top + 15 and spacecraft.get_landing_condition():
            return True
        return False

    def show_landing_conditions(self, display, font, c):
        """
        Indicate if the spacecraft has met the necessary landing conditions.
        (green lines at both sides when an attempt would be successful, otherwise red)
        :param display: Pygame screen surface
        :param font: indicators font
        :param c: indicators color
        """
        msg = font.render("|    |", False, c)
        msg_rect = msg.get_rect()
        msg_rect.center = (self.rect.center[0], self.rect.y)
        display.blit(msg, msg_rect)
