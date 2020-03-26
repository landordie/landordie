"""
menu_scene module.
"""
from .button import Button
from .scene_base import *
from .splash_scene import SplashScene
from .input_box import InputBox


class MenuScene(SceneBase):

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MenuScene.__instance is None:
            MenuScene()
        return MenuScene.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super().__init__()  # Call the super class (SceneBase) initialization method. This statement ensures that this
        # class inherits its behaviour from its Superclass. Abstract methods of all scenes (ProcessInput, Render,
        # Update, etc.), screen resolutions, text fonts, general text drawing methods and so on.

        if MenuScene.__instance is not None:
            raise Exception("This class is a MenuScene!")
        else:
            MenuScene.__instance = self

        # Start and quit buttons
        self.start_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2.2, BUTTON_WIDTH,
                                   BUTTON_HEIGHT), YELLOW, 'Start')
        self.accounts_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.7, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Accounts')
        self.options_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.4, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), GREEN, 'Options')
        self.quit_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.18, BUTTON_WIDTH
                                     , BUTTON_HEIGHT), RED, 'Quit')

        self.background = None
        self.logos = [pygame.image.load("frames/logo/LAND (" + str(x) + ").png") for x in range(1, 23)]
        self.logo_counter = 1
        self.current_logo = self.logos[0]
        self.x = 0

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Terminate on 'Esc' key
                self.terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.on_click(event):  # Switch to Splash scene
                    self.switch_to_scene(SplashScene(InputBox.boxes))
                elif self.accounts_button.on_click(event):  # Update scene and switch
                    from .accounts_scene import AccountsScene  # Avoiding circular dependencies
                    accounts_scene = AccountsScene.get_instance()
                    accounts_scene.update_all()
                    self.switch_to_scene(accounts_scene)
                elif self.options_button.on_click(event):  # Switch to Options scene
                    from .options_scene import OptionsScene  # Avoiding circular dependencies
                    self.switch_to_scene(OptionsScene.get_instance())
                elif self.quit_button.on_click(event):  # Quit button exits program
                    self.terminate()

    def render(self, screen):
        display = self.adjust_screen(screen)  # Surface
        # TODO: Write test to make sure self.background is not NONE
        # Background parallax effect
        # It works the same way as in the MenuScene instance
        image_width = self.background.get_rect().width
        rel_x = self.x % image_width  # The relative x of the image used for the parallax effect
        # Displaying the image based on the relative x and the image width
        display.blit(self.background, (rel_x - image_width, 0))

        # When the right end of the image reaches the right side of the screen
        # a new image starts displaying so we do not have any black spaces
        if rel_x < self.screen_width:
            display.blit(self.background, (rel_x, 0))
        self.x -= 1  # This decrement is what makes the image "move"

        self.control_logo()
        display.blit(self.current_logo, ((self.screen_width / 2 - self.current_logo.get_size()[0] / 2),
                                         (self.screen_height/4 - self.current_logo.get_size()[1] / 2)))
        # Update buttons
        self.start_button.update(display)
        self.accounts_button.update(display)
        self.options_button.update(display)
        self.quit_button.update(display)

    def control_logo(self):
        self.logo_counter += 1
        if self.logo_counter == 10000:
            self.logo_counter = 0

        if self.logo_counter % 5 == 0:
            self.current_logo = self.logos[(self.logos.index(self.current_logo)+1) % 22]

    # This method is used when changing the resolutions
    # It recalculates the relative positions of all buttons on the main menu screen and puts them where they should be
    def update_all(self):
        self.menu_button.rect.x,  self.menu_button.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2.2
        self.menu_button_2.rect.x,  self.menu_button_2.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.4
        self.menu_button_3.rect.x , self.menu_button_3.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.18
        self.menu_button_4.rect.x, self.menu_button_4.rect.y = \
            self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.7
