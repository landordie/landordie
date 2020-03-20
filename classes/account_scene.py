from .menu_scene import MenuScene
from .game_scene import *
from .button import Button
import pygame
from .input_box import InputBox


class AccountScene(SceneBase):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AccountScene.__instance is None:
            AccountScene()
        return AccountScene.__instance

    def __init__(self):
        if AccountScene.__instance is not None:
            raise Exception("This class is a MenuScene!")
        else:
            AccountScene.__instance = self

        SceneBase.__init__(self)
        self.menu_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.2, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW, 'Main Menu')

        self.login_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.7, BUTTON_WIDTH,
                                    BUTTON_HEIGHT), GREEN, 'Sign in')

        self.register_button = Button(
            (self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.4, BUTTON_WIDTH,
             BUTTON_HEIGHT), RED, 'Sign up')

        self.background = pygame.image.load("frames/BG.png")
        self.x = 0

        # Container for controls boxes
        self.button_cont_w, self.button_cont_h = self.screen_width / 2, self.screen_height / 3
        self.button_cont_x, self.button_cont_y = (self.screen_width / 2 - self.button_cont_w / 2), (self.screen_height / 5)
        self.button_cont = pygame.Surface((self.button_cont_w, self.button_cont_h)).convert_alpha()
        self.button_cont.fill(BLACK_HIGHLIGHT2)

        # Input boxes to change controls
        self.input_box1 = InputBox(self.button_cont_x * 1.7, self.button_cont_y + 50, '', 350, 33)
        self.input_box2 = InputBox(self.button_cont_x * 1.7, self.button_cont_y * 1.60 + 50, '', 350, 33)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_button.on_click(event):
                    menu = MenuScene.getInstance()
                    self.SwitchToScene(menu)

    def Update(self):
        pass

        # (!) When adding buttons to the start screen
        # (!) Add them here, in this method

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))

        # TODO: Write test to make sure self.background is not NONE
        # Background parallax effect
        image_width = self.background.get_rect().width
        # The relative x of the image used for the parallax effect
        rel_x = self.x % image_width
        # Displaying the image based on the relative x and the image width
        screen.get_surface().blit(self.background, (rel_x - image_width, 0))
        # When the right end of the image reaches the right side of the screen
        # a new image starts displaying so we do not have any black spaces
        if rel_x < self.screen_width:
            screen.get_surface().blit(self.background, (rel_x, 0))
        # This decrement is what makes the image "move"
        self.x -= 1
        # Update buttons
        self.menu_button.update(screen.get_surface())
        self.login_button.update(screen.get_surface())
        self.register_button.update(screen.get_surface())

        screen.get_surface().blit(self.button_cont,
                                  (self.button_cont_x, self.button_cont_y, self.button_cont_w, self.button_cont_h))

        self.draw_text(screen, "Username:", (self.button_cont_x * 1.4, self.button_cont_y * 1.42),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Password:", (self.button_cont_x * 1.4, self.button_cont_y * 2.03),
                      self.font_medium, WHITE)

        self.input_box1.draw(screen.get_surface())

        self.input_box2.draw(screen.get_surface())

    # This method is used when changing the resolutions
    # It recalculates the relative positions of all buttons on the main menu screen and puts them where they should be
    def update_all(self):
        self.menu_button.rect.x, self.menu_button.rect.y = self.screen_width / 2 - (
                    BUTTON_WIDTH / 2), self.screen_height / 1.2
        self.register_button.rect.x, self.register_button.rect.y = self.screen_width / 2 - (
                    BUTTON_WIDTH / 2), self.screen_height / 1.4
        self.login_button.rect.x, self.login_button.rect.y = self.screen_width / 2 - (
                    BUTTON_WIDTH / 2), self.screen_height / 1.7

