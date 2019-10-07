"""
Button Class
"""
import pygame as pg
import random
from constants import *


class Button:

    def __init__(self, rect, color, text, **kwargs):
        self.rect = pg.Rect(rect)
        self.color = color
        self.font = pg.font.SysFont('freesansbold.ttf', 20)
        self.text = self.font.render(text, True, BLACK)
        self.hovered = False

    def change_color(self):
        self.color = [random.randint(0, 150) for _ in range(3)]

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False

    def update(self, surface):
        """Update needs to be called every frame in the main loop."""
        self.check_hover()
        if self.hovered:
            surface.fill(WHITE, self.rect)
        surface.fill(self.color, self.rect.inflate(-4, -4))
        text_rect = self.text.get_rect()
        surface.blit(self.text, (self.rect.centerx - (text_rect.width/2), self.rect.centery - (text_rect.height/2) ))

