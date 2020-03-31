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
    """SplashScene subclass implementation."""

    def __init__(self):
        """Virtually private constructor which initializes the Splash scene."""
        super().__init__()  # Call the super class (SceneBase) initialization method. This
        # statement ensures that this class inherits its behaviour from its Superclass.
        # Abstract methods of all scenes (process_input(), update(), render(), etc.), screen
        # resolutions, text fonts, general text drawing methods and so on.

        self.star_field = StarField(self.screen_width, self.screen_height)  # Initialize the dynamic background

        self.splash_w, self.splash_h = self.screen_width / 1.4, self.screen_height / 1.3
        self.splash_x, self.splash_y = (self.screen_width / 2) - (self.splash_w / 2), \
                                       (self.screen_height / 2) - (self.splash_h / 2)
        self.controls_background = pygame.Surface((self.splash_w, self.splash_h)).convert_alpha()
        self.controls_background.fill(BLACK_HIGHLIGHT)

        self.background = pygame.image.load('frames/splash_BG.jpg')  # Load the background image
        # https://images.wallpaperscraft.com/image/texture_surface_dark_128260_1920x1080.jpg

        # Create the 'Continue' button
        self.continue_button = Button((self.screen_width / 2 - (BUTTON_WIDTH / 2),
                                       self.splash_h, BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW, 'Continue')

        self.controls = Controls.get_controls()  # Fetch the game controls

        # Set the spacecraft and anti-spacecraft controls accordingly using the fetched controls
        self.spacecraft_left, self.spacecraft_right, self.spacecraft_thrust = self.load_controls_images(1)
        self.a_spacecraft_left, self.a_spacecraft_right, self.a_spacecraft_shoot, self.a_spacecraft_cannon_left,\
            self.a_spacecraft_cannon_right = self.load_controls_images(2)

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
        display = self.adjust_screen(screen)  # Adjust the Splash scene screen (height and width) and get the surface
        display.blit(self.background, (0, 0))  # Display the background image
        self.star_field.draw_stars(display)  # Display the dynamic background image

        # Display the control button images' black background rectangle
        display.blit(self.controls_background, (self.splash_x, self.splash_y, self.splash_w, self.splash_h))

        # Draw Splash scene section indicators
        self.draw_text(screen, "Game Controls", (self.splash_x + self.splash_w / 2,
                                                 self.splash_y * 1.5), self.font_header, LIGHT_PURPLE)
        self.draw_text(screen, "Spacecraft: ", (self.splash_x * 2,
                                                self.splash_y + 100), self.font_player_num, WHITE)
        self.draw_text(screen, "Anti-spacecraft: ", (self.splash_x * 5,
                                                     self.splash_y + 100), self.font_player_num, WHITE)

        # Display the controls for the spacecraft player
        # on the splash screen
        display.blit(self.spacecraft_thrust, (self.splash_x * 2, self.splash_y + 150))
        self.draw_text(screen, "Thruster On", (self.splash_x * 1.5,
                                               self.splash_y + 200), self.font_freesans_bold, WHITE)

        display.blit(self.spacecraft_left, (self.splash_x * 2, self.splash_y + 250))
        self.draw_text(screen, "Rotate Left", (self.splash_x * 1.5,
                                               self.splash_y + 300), self.font_freesans_bold, WHITE)

        display.blit(self.spacecraft_right, (self.splash_x * 2, self.splash_y + 350))
        self.draw_text(screen, "Rotate Right", (self.splash_x * 1.5,
                                                self.splash_y + 400), self.font_freesans_bold, WHITE)

        # Display the controls for the anti-spacecraft player
        # on the splash screen
        display.blit(self.a_spacecraft_cannon_right, (self.splash_x * 5, self.splash_y + 125))
        self.draw_text(screen, "Cannon Right", (self.splash_x * 4.5,
                                                self.splash_y + 175), self.font_freesans_bold, WHITE)
        display.blit(self.a_spacecraft_cannon_left, (self.splash_x * 5, self.splash_y + 200))
        self.draw_text(screen, "Cannon Left", (self.splash_x * 4.5,
                                               self.splash_y + 250), self.font_freesans_bold, WHITE)
        display.blit(self.a_spacecraft_left, (self.splash_x * 5, self.splash_y + 350))  # 350
        self.draw_text(screen, "Move Left", (self.splash_x * 4.5,
                                             self.splash_y + 400), self.font_freesans_bold, WHITE)  # 400
        display.blit(self.a_spacecraft_right, (self.splash_x * 5, self.splash_y + 275))
        self.draw_text(screen, "Move Right", (self.splash_x * 4.5,
                                              self.splash_y + 325), self.font_freesans_bold, WHITE)
        display.blit(self.a_spacecraft_shoot, (self.splash_x * 5, self.splash_y + 425))
        self.draw_text(screen, "Shoot", (self.splash_x * 4.5,
                                         self.splash_y + 475), self.font_freesans_bold, WHITE)

        self.continue_button.update(display)  # Update the 'Continue' button
