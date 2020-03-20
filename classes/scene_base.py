import pygame
from constants import *


pygame.font.init()  # Initialize the pygame font objects


class SceneBase:
    """ This class is the Superclass of all the other scene classes - MenuScene(), GameScene(), SplashScene(),
    ResultsScene() and OptionsScene(). It creates 5 abstract methods - ProcessInput, Render, Update, SwitchToScene and
    Terminate. Each method is inherited by the above classes and overwritten with the functionallity required by the
    particular class.
        General purpose:
            1 - ProcessInput() - This method is responsible for processing all the events that occur in the environment
            (game window). Every frame a list of all the filltered events (the ones we care about - button presses,
            mouse movement, etc.) are passed to this method. It then executes the functionality specified for each event
            of interest.
            2 - Update() - This method's purpose is to update any variables within the frames. In our case the are left
            empty as no such updates are required by the program
            3 - Render() - Here, all the rendering for the certain scene occurs. This method is displaying all objects
            on the screen (backgrounds, sprites, pymunk shapes, terrain, etc.). It reflects any changes on variables as
            it is executed every frame.
            4 - SwitchToScene() - This method is used to change the focus of the main program from one scene to another.
            For example, when the Options button is clicked in the MenuScene the SwitchToScene method is setting the
            '.next' attribute of the current scene to OptionsScene(). That is how when the main program starts calling
            the Render() and ProcessInput() for the 'current_scene' variable, it starts displaying the OptionsScene.
            5 - Terminate() - This method sets the current scenes '.next' variable to None. That is how clicking on
            the 'X' (exit) button of the window stops the game.
    """
    screen_width = DEFAULT_WIDTH
    screen_height = DEFAULT_HEIGHT

    def __init__(self):
        self.next = self
        self.logged_in = False
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









