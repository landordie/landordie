"""
'input_box.py' module.
Used for player input when changing controls in the Options scene, logging in
and registering in Accounts scene and storing results in the Result scene.
"""
from constants import *
import pygame


class InputBox:
    """InputBox instance class."""

    def __init__(self, x, y, text='', w=100, h=35):
        """Virtually private constructor which initializes the input box for player input."""
        self.rect = pg.Rect(x, y, w, h)  # Set the rectangle coordinates along with its size
        self.color = BRIGHT_PURPLE  # Set the rectangle color (outline)
        self.text = text  # Set the text string inside the box
        self.txt_surface = FONT_BIG.render(text, True, WHITE)  # Set the text font and color
        self.active = False  # Boolean attribute for showing activity of a box (highlighting)

    def handle_event(self, event, box_type=1):
        """
        Handle event concerning the input box.
        :param event: rendered event
        :param box_type: 1 -> normal input box, 2 -> hidden symbols (password) box
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # On input box click
                self.active = not self.active  # Toggle the active variable to highlight the box
            else:
                self.active = False
        if box_type == 1:  # On normal box type
            if event.type == pg.KEYDOWN:  # Whenever a key is pressed display
                # the name of the key in the input box
                if self.active:  # If the box has been clicked on (is active)
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        if event.key == pg.K_UP:
                            self.text = 'Up'
                        elif event.key == pg.K_DOWN:
                            self.text = 'Down'
                        elif event.key == pg.K_LEFT:
                            self.text = 'Left'
                        elif event.key == pg.K_RIGHT:
                            self.text = 'Right'
                        elif event.key == pg.K_LSHIFT:
                            self.text = 'LShift'
                        elif event.key == pg.K_RSHIFT:
                            self.text = 'RShift'
                        elif event.key == pg.K_LCTRL:
                            self.text = 'LCtrl'
                        elif event.key == pg.K_RCTRL:
                            self.text = 'RCtrl'
                        elif event.key == pg.K_SPACE:
                            self.text = 'Space'
                        elif event.key == pg.K_LALT:
                            self.text = 'LAlt'
                        elif event.key == pg.K_RALT:
                            self.text = 'RAlt'
                        elif event.key == pg.K_RETURN:
                            self.text = 'Enter'
                        elif event.key == pg.K_TAB:
                            self.text = 'Tab'
                        elif event.key == pg.K_BACKSLASH:
                            self.text = 'BSlash'
                        elif event.key == pg.K_SLASH:
                            self.text = 'Slash'
                        elif event.key == pg.K_ASTERISK:
                            self.text = 'Asterisk'
                        else:
                            self.text = event.unicode.upper()
                        self.active = False
        if box_type == 2:  # On hidden symbols box type
            if event.type == pygame.KEYDOWN and self.active:  # If the box has been clicked on and a key is pressed
                # If the pressed button corresponds to a alphabetical char (a,b,c,d...,x,y,z)
                if event.unicode.isalnum() and len(self.text) < 16:
                    self.text += event.unicode
                # If the user would like to delete a char from the screen
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.text = self.text[:-1]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Toggle off the highlight (activity)
                self.active = False
        # Re-render the text.
        self.txt_surface = FONT_BIG.render(self.text, True, WHITE)
        # Change the current color of the input box.
        self.color = CYAN if self.active else BRIGHT_PURPLE

    def update(self):
        """Update input box. (resize if the input is too long)"""
        width = max(50, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen, hidden=False):
        """
        Draw the input box text on the screen.
        :param screen: current scene screen
        :param hidden: True when drawing passwords
        """
        if not hidden:  # If the box does not contain a password
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))  # Blit the text.
        else:  # Replace symbols with '*' and blit
            hidden_text = '*' * len(self.text)
            txt_surface = FONT_BIG.render(hidden_text, True, WHITE)
            screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 3)  # Blit the text rectangle

    def respond_to_resolution(self, new_x, new_y):
        """
        Adjust the input box position according to the screen resolution.
        :param new_x: new x-axis coordinate of the input box rectangle
        :param new_y: new y-axis coordinate of the input box rectangle
        """
        self.rect.x = new_x
        self.rect.y = new_y
