"""
    Menu Module (Subclass of Scene Base)
"""
from load_images import load_images, update as title_update
from .scene_base import *
from .game_scene import GameScene
from .splash_scene import SplashScene
from .button import Button


class MenuScene(SceneBase):
    """Menu Scene Instance Class"""
    
    def __init__(self):
        SceneBase.__init__(self)
        
        # Set screen dimension attributes
        self.width = M_SCREEN_WIDTH
        self.height = M_SCREEN_HEIGHT

        # Start and Quit buttons
        self.menu_button = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Start')
        self.menu_button_2 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.5, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Quit')

    def ProcessInput(self, events, pressed_keys):
        """Event loop method to handle events"""
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN
                                                                                   and event.button == 1 and
                                                                                   self.menu_button_2.on_click(event)):
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                self.SwitchToScene(SplashScene())

    def Render(self, screen):
        """Render screen method which draws the buttons and the background"""
        # Load the logo frames
        game_title = load_images("frames/big")
        title_surfaces = game_title.values()

        screen.get_surface().fill(BLACK)

        # Update buttons
        self.menu_button.update(screen.get_surface())
        self.menu_button_2.update(screen.get_surface())

        # Update title
        title_update(title_surfaces, screen)
