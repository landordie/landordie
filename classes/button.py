"""
Button Class
"""
import random

import pygame as pg
from constants import *



class Button:
    """Button Instance Class"""
    
    def __init__(self, rect, color, text, **kwargs):
        self.rect = pg.Rect(rect)
        self.color = color
        self.font = pg.font.SysFont('freesansbold.ttf', 30)
        self.text = self.font.render(text, True, BLACK)
        self.hovered = False


    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False
    
    def check_hover(self):
        """Check if the mouse cursor is over a button and if so play the hover sound"""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                pg.mixer.Sound(HOVER_SOUND).play()  # play sound
        else:
            self.hovered = False

    def wh_text(self):
        """Text rectangle width and height as tuple"""
        text_rect = self.text.get_rect()
        return text_rect.width, text_rect.height

    def update(self, surface):
        """Update needs to be called every frame in the main loop"""
        self.check_hover()
        if self.hovered:
            surface.fill(WHITE, self.rect)
        surface.fill(self.color, self.rect.inflate(-4, -4))

        text_width, text_height = self.wh_text()
        surface.blit(self.text, (self.rect.centerx - (text_width / 2), self.rect.centery - (text_height / 2)))
