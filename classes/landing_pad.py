"""
Landing pad class
"""
import pygame as pg
import pymunk as pm
import random
from .sprite_class import Sprite
from .helper import flipy


class LandingPad(Sprite):
    def __init__(self, width, height):
        super().__init__('frames/landing_pad.png')
        self.rect.top = random.randint(height // 1.7, height // 1.5)
        self.rect.right = random.randint(155, width - 100)
        self.mask = pg.mask.from_surface(self.image)
        self.landable = True

    # This method generates and returns a pymunk segment object which is used to
    # detect physics based collision between the spaceship and the landing pad
    # We are doing it this way because we don't track collision based on sprites but on pymunk physics objects
    def pymunk_pad(self, space, height):
        pm_pad = pm.Segment(space.static_body, flipy((self.rect.left + 14, self.rect.top + 16), height),
                            flipy((self.rect.right - 14, self.rect.top + 16), height), 5)
        pm_pad.collision_type = 4
        return pm_pad

    # If these conditions are met, the method returns whether the spaceship has landed
    # on the landing pad (successfully or not)
    def check_for_landing_attempt(self, spacecraft):
        if spacecraft.rect.right < self.rect.right and \
                spacecraft.rect.left > self.rect.left and spacecraft.rect.bottom <= self.rect.top + 15 \
                and spacecraft.get_landing_condition():
            return True

    def show_landing_conditions(self, display, font, c):
        msg = font.render("|    |", False, c)
        msg_rect = msg.get_rect()
        msg_rect.center = (self.rect.center[0], self.rect.y)
        display.blit(msg, msg_rect)
