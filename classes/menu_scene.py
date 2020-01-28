from load_images import load_images, update as title_update
from .scene_base import *
from .game_scene import GameScene
from .splash_scene import SplashScene
from .options_scene import OptionsScene
from .button import Button


class MenuScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.width = M_SCREEN_WIDTH
        self.height = M_SCREEN_HEIGHT

        # Start and Quit buttons
        self.menu_button = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Start')
        self.menu_button_2 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.25, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Quit')
        self.menu_button_3 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.50, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), GREEN, 'Options')

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                self.SwitchToScene(SplashScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button_3.on_click(event):
                self.SwitchToScene(OptionsScene())

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