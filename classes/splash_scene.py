"""
'splash_scene.py' module.
Used in creating a Splash scene (window).
"""
from .scene_base import *
from .game_scene import GameScene
from .button import Button
from .controls import Controls
from .star_field import StarField


class SplashScene(SceneBase):
    """SplashScene subclass."""

    def __init__(self, box_texts=None):
        """Virtually private constructor which initializes the Splash scene."""
        super().__init__()  # Call the super class (SceneBase) initialization method. This
        # statement ensures that this class inherits its behaviour from its Superclass.
        # Abstract methods of all scenes (process_input(), update(), render(), etc.), screen
        # resolutions, text fonts, general text drawing methods and so on.

        self.star_field = StarField(self.screen_width, self.screen_height)
        self.splash_w, self.splash_h = self.screen_width / 1.4, self.screen_height / 1.3
        self.splash_x, self.splash_y = (self.screen_width / 2) - (self.splash_w / 2),\
                                       (self.screen_height / 2) - (self.splash_h / 2)

        self.controls_background = pygame.Surface((self.splash_w, self.splash_h)).convert_alpha()
        self.controls_background.fill(BLACK_HIGHLIGHT)
        self.background = pygame.image.load('frames/splash_BG.jpg')
        # https://images.wallpaperscraft.com/image/texture_surface_dark_128260_1920x1080.jpg

        # Continue button
        self.continue_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2),
                                       self.splash_h, BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW, 'Continue')

        if not box_texts:
            self.controls = DEFAULT_CONTROLS
        else:
            self.controls = box_texts
        self.player1_left, self.player1_right, self.player1_thrust = self.load_controls_images(1)
        self.player2_left, self.player2_right, self.player2_shoot, self.player2_cannon_left, self.player2_cannon_right \
            = self.load_controls_images(2)
        # update controls
        Controls.update(self.controls)

    def load_controls_images(self, player_num):
        """
        Unpack the images required to display the controls in the Splash scene.
        :param player_num: 1 -> spacecraft player, 2 -> anti-spacecraft player
        :return: player control images
        """
        if player_num == 1:  # Load spacecraft control images
            rotate_left = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[0]}.png')
            thrust = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[1]}.png')
            rotate_right = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[2]}.png')
            return rotate_left, rotate_right, thrust
        elif player_num == 2:  # Load anti-spacecraft control images
            move_left = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[3]}.png')
            move_right = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[5]}.png')
            shoot = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[7]}.png')
            cannon_left = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[6]}.png')
            cannon_right = pygame.image.load(
                f'frames/keys/Keyboard & Mouse/Light/Keyboard_White_{self.controls[4]}.png')
            return move_left, move_right, shoot, cannon_left, cannon_right
        else:
            raise ValueError("Error when specifying player number.")

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Terminate on 'Esc' button
                self.terminate()
            # On left mouse button click and if the mouse is on the 'Continue' button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.continue_button.on_click(event):
                self.switch_to_scene(GameScene())  # Switch to a GameScene instance

    def update(self):
        self.star_field.set_params(self.screen_width, self.screen_height)  # Update the background image

    def render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))

        screen.get_surface().blit(self.background, (0, 0))
        self.star_field.draw_stars(screen.get_surface())

        screen.get_surface().blit(self.controls_background,
                                  (self.splash_x, self.splash_y, self.splash_w, self.splash_h))

        self.draw_text(screen, "Game Controls", (self.splash_x + self.splash_w / 2,
                                                 self.splash_y * 1.5), self.font_header, LIGHT_PURPLE)
        self.draw_text(screen, "Spacecraft: ", (self.splash_x * 2,
                                                self.splash_y + 100), self.font_player_num, WHITE)
        self.draw_text(screen, "Anti-spacecraft: ", (self.splash_x * 5,
                                                     self.splash_y + 100), self.font_player_num, WHITE)

        # Display the controls for Player 1 (controlling the ship)
        # on the splash screen

        screen.get_surface().blit(self.player1_thrust, (self.splash_x * 2, self.splash_y + 150))
        self.draw_text(screen, "Thruster On", (self.splash_x * 1.5,
                                               self.splash_y + 200), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(self.player1_left, (self.splash_x * 2, self.splash_y + 250))
        self.draw_text(screen, "Rotate Left", (self.splash_x * 1.5,
                                               self.splash_y + 300), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(self.player1_right, (self.splash_x * 2, self.splash_y + 350))
        self.draw_text(screen, "Rotate Right", (self.splash_x * 1.5,
                                                self.splash_y + 400), self.font_freesans_bold, WHITE)

        # Display the controls for Player 2 (controlling the tank)
        # on the splash screen

        screen.get_surface().blit(self.player2_cannon_right, (self.splash_x * 5, self.splash_y + 125))
        self.draw_text(screen, "Cannon Right", (self.splash_x * 4.5,
                                                self.splash_y + 175), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(self.player2_cannon_left, (self.splash_x * 5, self.splash_y + 200))
        self.draw_text(screen, "Cannon Left", (self.splash_x * 4.5,
                                               self.splash_y + 250), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(self.player2_left, (self.splash_x * 5, self.splash_y + 350))  # 350
        self.draw_text(screen, "Move Left", (self.splash_x * 4.5,
                                             self.splash_y + 400), self.font_freesans_bold, WHITE)  # 400
        screen.get_surface().blit(self.player2_right, (self.splash_x * 5, self.splash_y + 275))
        self.draw_text(screen, "Move Right", (self.splash_x * 4.5,
                                              self.splash_y + 325), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(self.player2_shoot, (self.splash_x * 5, self.splash_y + 425))
        self.draw_text(screen, "Shoot", (self.splash_x * 4.5,
                                         self.splash_y + 475), self.font_freesans_bold, WHITE)

        self.continue_button.update(screen.get_surface())
        pygame.display.update()
