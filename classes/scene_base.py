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


# Unpacking the images required to display the controls in the splash screen
# If an incorrect player ID is used, an error will be raised
# (!) TODO: Resize the images for the buttons to 60x60/70x70 so that they fit better (!)
def load_controls_images(player):
    if player == 1:
        # Load player 1 images
        rotate_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_A.png')
        rotate_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_D.png')
        thrust = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_W.png')
        return rotate_left, rotate_right, thrust
    elif player == 2:
        # Load player 2 images
        move_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Left.png')
        move_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Right.png')
        shoot = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Space.png')
        cannon_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Down.png')
        cannon_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Up.png')
        return move_left, move_right, shoot, cannon_left, cannon_right
    else:
        raise ValueError("Error when specifying player number.")


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
        self.font_arial_black = pygame.font.SysFont('Arial Black', 18)
        self.font_verdana = pygame.font.SysFont('Verdana', 25)
        self.font_arial_black_large = pygame.font.SysFont('Arial Black', 50)
        self.font_verily_mono = pygame.font.SysFont('Verily Serif Mono', 27)
        self.font_consolas = pygame.font.SysFont('Consolas', 30)
        self.font_freesans_bold = pygame.font.SysFont("Freesans Bold", 35)

    @staticmethod
    def draw_text(screen, message, position, font, color=(0, 0, 0)):
        text = font.render(message, False, color)
        text_rect = text.get_rect(center=position)
        screen.get_surface().blit(text, text_rect)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)









