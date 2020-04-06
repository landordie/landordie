"""
'menu_scene.py' module.
Used in instantiation of the Menu scene (window).
"""
from .button import Button
from .scene_base import *
from .splash_scene import SplashScene


class MenuScene(SceneBase):
    """MenuScene singleton subclass."""
    __instance = None

    @staticmethod
    def get_instance():
        """
        Static access method. Ensures the singularity of a class instance.
        :return: MenuScene class instance
        """
        if MenuScene.__instance is None:
            MenuScene()
        return MenuScene.__instance

    def __init__(self):
        """Virtually private constructor which initializes the Menu scene."""
        super().__init__()  # Call the super class (SceneBase) initialization method. This
        # statement ensures that this class inherits its behaviour from its Superclass.
        # Abstract methods of all scenes (process_input(), update(), render(), etc.), screen
        # resolutions, text fonts, general text drawing methods and so on.

        # Check if there are any instances of the class already created
        if MenuScene.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MenuScene.__instance = self

        # Create buttons (Start, Accounts, Options, Quit)
        self.start_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2.2,
                                    BUTTON_WIDTH,BUTTON_HEIGHT), YELLOW, 'Start')
        self.accounts_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.7,
                                       BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Accounts')
        self.options_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.4,
                                      BUTTON_WIDTH,BUTTON_HEIGHT), GREEN, 'Options')
        self.quit_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.18,
                                   BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Quit')

        self.background = pg.image.load("Assets/frames/BG.png")

        # Set the background glowing title logo
        self.logos = [pg.image.load("Assets/frames/logo/LAND (" + str(x) + ").png") for x in range(1, 23)]
        self.logo_counter = 1
        self.current_logo = self.logos[0]
        self.x = 0  # Variable used in simulating the x-axis 'movement' of the background image

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # Terminate on 'Esc' key
                self.terminate()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # On left mouse button click
                if self.start_button.on_click(event):  # Switch to Splash scene
                    self.switch_to_scene(SplashScene())
                elif self.accounts_button.on_click(event):  # Update scene and switch
                    from .accounts_scene import AccountsScene  # Avoiding circular dependencies
                    accounts_scene = AccountsScene.get_instance()
                    accounts_scene.update()
                    self.switch_to_scene(accounts_scene)
                elif self.options_button.on_click(event):  # Switch to Options scene
                    from .options_scene import OptionsScene  # Avoiding circular dependencies
                    self.switch_to_scene(OptionsScene.get_instance())
                elif self.quit_button.on_click(event):  # Quit button exits program
                    self.terminate()

    def update(self):
        """Recalculate the relative position of all buttons and update (respond to resolution change)."""
        self.start_button.rect.x,  self.start_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2.2
        self.accounts_button.rect.x, self.accounts_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.7
        self.options_button.rect.x,  self.options_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.4
        self.quit_button.rect.x, self.quit_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.18

    def render(self, screen):
        display = self.adjust_screen(screen)  # Surface
        # TODO: Write test to make sure self.background is not NONE
        self.parallax_effect(display)  # Initialize the parallax effect

        self.control_logo()
        display.blit(self.current_logo, ((self.screen_width / 2 - self.current_logo.get_size()[0] / 2),
                                         (self.screen_height/4 - self.current_logo.get_size()[1] / 2)))
        # Update buttons
        self.start_button.update(display)
        self.accounts_button.update(display)
        self.options_button.update(display)
        self.quit_button.update(display)

    def control_logo(self):
        """Background logo glow effect animation method"""
        # Switch between logo images to simulate the glow effect
        self.logo_counter += 1
        if self.logo_counter == 10000:
            self.logo_counter = 0

        if self.logo_counter % 5 == 0:
            self.current_logo = self.logos[(self.logos.index(self.current_logo) + 1) % 22]  # There are 22 logo images
