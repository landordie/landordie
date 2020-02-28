import pygame
from classes.sprite_class import Sprite


class LandingPad(Sprite):
    def __init__(self):
        super().__init__('frames/landing_pad.png')
        self.rect.top = 500
        self.rect.left = 500
        self.mask = pygame.mask.from_surface(self.image)

    def check_for_landing_attempt(self, spacecraft):
        if spacecraft.rect.right < self.rect.right and \
                spacecraft.rect.left > self.rect.left and spacecraft.rect.bottom <= self.rect.top + 15 \
                and spacecraft.get_landing_condition():
            return True
