"""
Sprite class
"""
import pygame
from math import degrees
from pymunk import Vec2d
from constants import flipy


class Sprite(pygame.sprite.Sprite):
    """ Changing the Sprite class to work for our solution - to create static objects(background, obstacles, etc.)"""

    def __init__(self, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()

    def get_attachment_coordinates(self, pymunk_body, height):
        rotated_img = pygame.transform.rotate(self.image,
                                              degrees(pymunk_body.angle))
        position = flipy(pymunk_body.position, height)
        offset = Vec2d(rotated_img.get_size()) / 2.
        position -= offset
        return position, rotated_img
