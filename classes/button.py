"""
Button Class
"""
import random

import pygame as pg
from PyMunk.constants import *


class Button:

    def __init__(self, rect, color, text, **kwargs):
        self.rect = pg.Rect(rect)
        self.color = color
        self.font = pg.font.SysFont('freesansbold.ttf', 30)
        self.text = self.font.render(text, True, BLACK)
        self.hovered = False

    def change_color(self):
        """
        Not used yet
        """
        self.color = [random.randint(0, 150) for _ in range(3)]

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                pg.mixer.Sound(HOVER_SOUND).play()  # improve?
        else:
            self.hovered = False

    def wh_text(self):
        """
        Text rectangle width and height as tuple
        """
        text_rect = self.text.get_rect()
        return text_rect.width, text_rect.height

    def update(self, surface):
        """
        Update needs to be called every frame in the main loop.
        """
        self.check_hover()
        if self.hovered:
            surface.fill(WHITE, self.rect)
        surface.fill(self.color, self.rect.inflate(-4, -4))

        text_width, text_height = self.wh_text()
        surface.blit(self.text, (self.rect.centerx - (text_width / 2), self.rect.centery - (text_height / 2)))
