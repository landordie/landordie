import pygame
from classes.sprite_class import Sprite
import random


class LandingPad(Sprite):
    def __init__(self, width, height):
        super().__init__('frames/landing_pad.png')
        self.rect.top = random.randint(height // 1.7, height // 1.5)
        self.rect.right = random.randint(155, width)
        self.mask = pygame.mask.from_surface(self.image)

    def check_for_landing_attempt(self, spacecraft):
        if spacecraft.rect.right < self.rect.right and \
                spacecraft.rect.left > self.rect.left and spacecraft.rect.bottom <= self.rect.top + 15 \
                and spacecraft.get_landing_condition():
            return True
