"""
'sprite_class.py' module.
Used in creating Sprite instances (spacecraft, anti-spacecraft, icons etc.)
"""
import pygame
from math import degrees
from pymunk.vec2d import Vec2d
from .helper import flipy


class Sprite(pygame.sprite.Sprite):
    """Sprite class implementation"""

    def __init__(self, image_file):
        """
        Virtually private constructor which initializes the Sprite instance.
        :param image_file: image file location
        """
        super().__init__()
        self.image = pygame.image.load(image_file)  # Load the image file
        self.rect = self.image.get_rect()  # Get the image rectangle

    def get_attachment_coordinates(self, pm_body, height):
        # TODO: Make sure to explain this in report
        """
        Determine the exact position the Pygame object must be placed at. Convert Pymunk
        coordinates into Pygame ones and also ensure that the Sprite rotates along with
        the Pymunk body. The Pymunk angles are in radians whereas the Pygame ones are in degrees.
        :param pm_body: Pymunk body
        :param height: current screen height
        :return: adjusted Sprite position, rotated Sprite image
        """
        rotated_img = pygame.transform.rotate(self.image, degrees(pm_body.angle))
        position = flipy(pm_body.position, height)
        offset = Vec2d(rotated_img.get_size()) / 2.  # Get the image offset
        position -= offset  # Adjust the position of the Pygame Sprite
        return position, rotated_img
