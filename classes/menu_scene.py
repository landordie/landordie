from load_images import load_images, update as title_update
from .button import Button
from .game_scene import GameScene
from .scene_base import *
from .splash_scene import SplashScene
from .input_box import InputBox


class MenuScene(SceneBase):

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MenuScene.__instance == None:
            MenuScene()
        return MenuScene.__instance

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        """ Virtually private constructor. """
        if MenuScene.__instance != None:
            raise Exception("This class is a MenuScene!")
        else:
            MenuScene.__instance = self

        SceneBase.__init__(self)

        # Start and Quit buttons
        self.menu_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Start')
        self.menu_button_2 = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.53, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), GREEN, 'Options')
        self.menu_button_3 = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.25, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Quit')

        self.background = None
        self.x = 0

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_button_2.on_click(event):
                    from .options_scene import OptionsScene
                    self.SwitchToScene(OptionsScene.getInstance())
                elif self.menu_button.on_click(event):  # start button
                    self.SwitchToScene(SplashScene(InputBox.boxes))
                elif self.menu_button_3.on_click(event):  # quit button
                    self.Terminate()

    def Update(self):
        pass

    # (!) When adding buttons to the start screen
    # (!) Add them here, in this method
    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))

        # TODO: Write test to make sure self.background is not NONE
        # Background parallax effect
        image_width = self.background.get_rect().width
        rel_x = self.x % image_width
        screen.get_surface().blit(self.background, (rel_x - image_width, 0))
        if rel_x < self.screen_width:
            screen.get_surface().blit(self.background, (rel_x, 0))
        self.x -= 1

        # Update buttons
        self.menu_button.update(screen.get_surface())
        self.menu_button_2.update(screen.get_surface())
        self.menu_button_3.update(screen.get_surface())

    def update_all(self):
        self.menu_button.rect.x,  self.menu_button.rect.y = self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 2
        self.menu_button_2.rect.x,  self.menu_button_2.rect.y = self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.53
        self.menu_button_3.rect.x , self.menu_button_3.rect.y = self.screen_width / 2 - (BUTTON_WIDTH / 2), self.screen_height / 1.25