import pygame
from classes.sprite_class import Sprite


class LandingPad(Sprite):
    def __init__(self):
        super().__init__('frames/landing_pad.png', 500,
                         500)
        self.mask = pygame.mask.from_surface(self.image)
