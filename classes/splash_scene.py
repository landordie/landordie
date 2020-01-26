from .scene_base import *
from .game_scene import GameScene
from .button import Button


class SplashScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.width = S_SCREEN_WIDTH
        self.height = S_SCREEN_HEIGHT

        # Continue button
        self.splash_button = Button((self.width / 2 - (BUTTON_WIDTH / 2),
                                     self.height / 1.2, BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW, 'Continue')

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.splash_button.on_click(event):
                self.SwitchToScene(GameScene())

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((S_SCREEN_WIDTH, S_SCREEN_HEIGHT))
        splash_w, splash_h = 700, 630
        splash_x, splash_y = (self.width/2) - \
            (splash_w/2), (self.height/2) - (splash_h/2)

        controls_background = pygame.Surface(
            (splash_w, splash_h)).convert_alpha()
        controls_background.fill(BLACK_HIGHLIGHT)
        logo = pygame.image.load('frames/Landordie.png')
        background = pygame.image.load('frames/backgr.png')

        player1_left, player1_right, player1_thrust = load_controls_images(1)
        player2_left, player2_right, player2_shoot, player2_cannon_left, player2_cannon_right = load_controls_images(2)

        screen.get_surface().fill(WHITE)

        screen.get_surface().blit(background, (0, 0))
        screen.get_surface().blit(controls_background,
                                  (splash_x, splash_y, splash_w, splash_h))
        screen.get_surface().blit(logo, (splash_x, splash_y))

        self.draw_text(screen, "Game Controls", (splash_x + (splash_w/1.5),
                                                 splash_y * 1.7), self.font_arial_black_large, (140, 123, 192))
        self.draw_text(screen, "Player 1: ", (splash_x + (splash_w/3.75),
                                              splash_y + 100), self.font_verdana, (255, 255, 255))
        self.draw_text(screen, "Player 2: ", (splash_x + 535,
                                              splash_y + 100), self.font_verdana, (255, 255, 255))

        # Display the controls for Player 1 (controlling the ship)
        # on the splash screen

        screen.get_surface().blit(player1_thrust, (splash_x + 125, splash_y + 150))
        self.draw_text(screen, "Thruster On", (splash_x + 175,
                                               splash_y + 150), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(player1_left, (splash_x + 50, splash_y + 250))
        self.draw_text(screen, "Rotate Left", (splash_x + 95,
                                               splash_y + 250), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(player1_right, (splash_x + 200, splash_y + 250))
        self.draw_text(screen, "Rotate Right", (splash_x + 255,
                                                splash_y + 250), self.font_freesans_bold, WHITE)

        # Display the controls for Player 2 (controlling the tank)
        # on the splash screen

        screen.get_surface().blit(player2_cannon_right, (splash_x + 475, splash_y + 150))
        self.draw_text(screen, "Cannon Right", (splash_x + 525,
                                                splash_y + 150), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_cannon_left, (splash_x + 475, splash_y + 350))
        self.draw_text(screen, "Cannon Left", (splash_x + 525,
                                                splash_y + 350), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_left, (splash_x + 375, splash_y + 250))
        self.draw_text(screen, "Move Left", (splash_x + 420,
                                             splash_y + 250), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_right, (splash_x + 575, splash_y + 250))
        self.draw_text(screen, "Move Right", (splash_x + 625,
                                              splash_y + 250), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_shoot, (splash_x + 475, splash_y + 450))
        self.draw_text(screen, "Shoot", (splash_x + 525,
                                         splash_y + 460), self.font_freesans_bold, WHITE)

        self.splash_button.update(screen.get_surface())
        pygame.display.update()