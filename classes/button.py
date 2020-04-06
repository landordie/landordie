"""
'button.py' module.
Used in the creation of all the buttons in the program.
"""
from constants import *


class Button:
    """Button instance class implementation."""

    def __init__(self, rect_size, color, text):
        """
        Button instance constructor.
        :param rect_size: size of the button rectangle
        :param color: color of the button rectangle
        :param text: button text string
        """
        self.rect = pg.Rect(rect_size)
        self.color = color
        self.font = FONT_SMALL_PLUS
        self.text_string = text
        self.text = self.font.render(text, True, WHITE)
        self.hovered = False
        self.image = pg.image.load("Assets/frames/Table_01.png")
        self.active_image = pg.image.load("Assets/frames/Table_01_active.png")

    def on_click(self, event):
        """
        Check for a button click.
        :param event: program event
        :return: True if the button is clicked and False otherwise
        """
        if self.rect.collidepoint(event.pos):
            return True
        return False

    def check_hover(self):
        """Play a sound if the mouse is hovering over a button."""
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                pg.mixer.Sound(HOVER_SOUND).play()
        else:
            self.hovered = False

    def wh_text(self):
        """
        Get the width and height of the text rectangle.
        :return: text rectangle width and height tuple
        """
        text_rect = self.text.get_rect()
        return text_rect.width, text_rect.height

    def update(self, surface):
        """
        Update button text position and image.
        :param surface: screen surface
        """
        self.check_hover()
        if self.hovered:  # Switch to active image of the button when hovered over
            surface.blit(self.active_image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))

        # Update button text position
        text_width, text_height = self.wh_text()
        surface.blit(self.text, (self.rect.centerx - (text_width / 2), self.rect.centery + 5))
