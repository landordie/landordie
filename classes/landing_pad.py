import pygame as pg
import pymunk as pm
from classes.sprite_class import Sprite
import random

from constants import flipy


class LandingPad(Sprite):
    def __init__(self, width, height):
        super().__init__('frames/landing_pad.png')
        self.rect.top = random.randint(height // 1.7, height // 1.5)
        self.rect.right = random.randint(155, width - 100)
        self.mask = pg.mask.from_surface(self.image)

    def pymunk_pad(self, space, height):
        return pm.Segment(space.static_body, flipy((self.rect.left + 14, self.rect.top + 16), height),
                          flipy((self.rect.right - 14, self.rect.top + 16), height), 5)

    def check_for_landing_attempt(self, spacecraft):
        if spacecraft.rect.right < self.rect.right and \
                spacecraft.rect.left > self.rect.left and spacecraft.rect.bottom <= self.rect.top + 15 \
                and spacecraft.get_landing_condition():
            return True
