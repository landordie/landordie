from load_images import load_images, update as title_update
from .button import Button
from .game_scene import GameScene
from .scene_base import *
from .splash_scene import SplashScene


class MenuScene(SceneBase):
    def __init__(self, os=''):
        SceneBase.__init__(self)
        self.width = M_SCREEN_WIDTH
        self.height = M_SCREEN_HEIGHT

        # Start and Quit buttons
        self.menu_button = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Start')
        self.menu_button_2 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.53, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), GREEN, 'Options')
        self.menu_button_3 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.25, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Quit')
        self.os = os

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_button_2.on_click(event):
                    from .options_scene import OptionsScene
                    self.SwitchToScene(OptionsScene())
                elif self.menu_button.on_click(event):  # start button
                    self.SwitchToScene(SplashScene(self.os))
                elif self.menu_button_3.on_click(event):  # quit button
                    self.Terminate()

    def Update(self):
        pass

    # (!) When adding buttons to the start screen
    # (!) Add them here, in this method
    def Render(self, screen):

        game_title = load_images("frames/big")
        title_surfaces = game_title.values()

        screen.get_surface().fill(BLACK)

        # Update buttons
        self.menu_button.update(screen.get_surface())
        self.menu_button_2.update(screen.get_surface())
        self.menu_button_3.update(screen.get_surface())

        # Update title
        title_update(title_surfaces, screen)
