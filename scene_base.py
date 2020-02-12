import pygame
from constants import *


pygame.font.init()
# (!) REMEMBER (!)
# When changing scenes, resolution is hardcoded
#


# Tuple unpacking for text display
def __text_objects(text, font):
    surface = font.render(text, True, BLACK)
    return surface, surface.get_rect()


# Method used to display text
# It's used on multiple occasions that's why it's taken out as a separate method
# Args: screen -> pygame.display object
#       text -> string you want displayed
#       size -> the size of the string (different lengths need different size)
#       font -> name of the font
def display_text(screen, text, font, size):
    screen = screen.get_surface()
    width, height = screen.get_size()
    font = pygame.font.Font(font, size)
    surface, rect = __text_objects(text, font)
    rect.center = ((width / 2), (height / 4))
    screen.blit(surface, rect)
    pygame.display.update()


class SceneBase:
    def __init__(self):
        self.next = self
        # Fonts:
        self.font_medium = pygame.font.Font(DEFAULT_FONT, 18)
        self.font_playernum = pygame.font.Font(DEFAULT_FONT, 17)
        self.font_header = pygame.font.Font(DEFAULT_FONT, 50)
        self.font_warning = pygame.font.Font(DEFAULT_FONT, 27)
        self.font_freesans_bold = pygame.font.Font(DEFAULT_FONT, 15)
        self.press2s = pygame.font.Font("PressStart2P.ttf", 14)

    @staticmethod
    def draw_text(screen, message, position, font, color=(0, 0, 0)):
        text = font.render(message, False, color)
        text_rect = text.get_rect(center=position)
        screen.get_surface().blit(text, text_rect)

    # Using this method mainly for testing
    # The game logic will be implemented in the Update() method
    def ProcessInput(self, events, pressed_keys):
        print("(!) Override in child class (!)")

    def Update(self):
        print("(!) Override in child class (!)")

    def Render(self, screen):
        print("(!) Override in child class (!)")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)









