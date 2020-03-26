"""
'scene_base.py' module.
Contains SceneBase abstract superclass.
"""
import pygame
from constants import *
pygame.font.init()  # Initialize the Pygame font objects


class SceneBase:
    """
    This class is the superclass of all the other scene classes - MenuScene, SplashScene, AccountsScene
    GameScene and ResultScene. It defines 7 abstract methods - process_input(), update(), render(),
    switch_to_scene(), terminate(), adjust_screen() and draw_text(). Each method is inherited by the
    above classes and overwritten with the functionality required by the particular class.
    """

    def __init__(self):
        """Virtually private constructor which initializes the SceneBase superclass."""
        self.screen_width = DEFAULT_WIDTH
        self.screen_height = DEFAULT_HEIGHT
        self.next = self
        # Fonts:
        self.font_medium = pygame.font.Font(DEFAULT_FONT, 18)
        self.font_player_num = pygame.font.Font(DEFAULT_FONT, 17)
        self.font_header = pygame.font.Font(DEFAULT_FONT, 50)
        self.font_warning = pygame.font.Font(DEFAULT_FONT, 27)
        self.font_freesans_bold = pygame.font.Font(DEFAULT_FONT, 15)
        self.press2s = pygame.font.Font("PressStart2P.ttf", 14)

    def process_input(self, events, pressed_keys):
        """
        Process all the events that occur in the environment (game window). Every frame
        a list of all the filtered events (the ones we care about - button presses,
        mouse movement, etc.) are passed to this method. It then executes the functionality
        specified for each event of interest.
        :param events: program scene event
        :param pressed_keys: pressed keys input
        """
        print("(!) Override in child class (!)")

    def update(self):
        """Update any variables (attributes) within the frames."""
        print("(!) Override in child class (!)")

    def render(self, screen):
        """
        Render the scene by displaying all objects on the screen (backgrounds, sprites, Pymunk
        shapes, terrain, etc.). It reflects any changes on variables as it is executed every frame.
        :param screen: scene screen (window)
        """
        print("(!) Override in child class (!)")

    def switch_to_scene(self, next_scene):
        """
        Change the focus of the main program from one scene to another. For example, when the Options
        button is clicked in the Menu scene the switch_to_scene() method is setting the '.next' attribute
        of the current scene to an OptionsScene instance. This changes the 'current_scene' variable in the
        main module to the OptionsScene singleton instance. Now the program is operating with the new scene
        methods instead.
        :param next_scene: scene instance to switch to
        """
        self.next = next_scene

    def terminate(self):
        """
        Set the current scene '.next' variable to None. That is how clicking on the 'X' (exit) button
        of the window stops the game. (Essentially calls the switch_to_scene() method with 'next_scene'
        parameter set to None)
        """
        self.switch_to_scene(None)

    def adjust_screen(self, screen):
        """
        Update screen changes (resolution) and return the new surface
        :param screen:
        :return: surface of the screen
        """
        screen.set_mode((self.screen_width, self.screen_height))  # Set the screen size
        return screen.get_surface()  # Get the surface of the screen

    @staticmethod
    def draw_text(screen, message, position, font, color=(0, 0, 0)):
        """
        Draw text on the given screen surface
        :param screen: screen
        :param message: text message to draw
        :param position: position of the text message
        :param font: font of text message
        :param color: color of text message
        """
        text = font.render(message, False, color)
        text_rect = text.get_rect(center=position)
        screen.get_surface().blit(text, text_rect)
