import math
import pygame
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

from .button import *
from load_images import load_images
from load_images import update as title_update
from constants import *
from .anti_space_craft import AntiSpaceCraft
from classes.Spacecraft import Spacecraft

pygame.font.init()
# (!) REMEMBER (!)
# When changing scenes, resolution is hardcoded
#


# Tuple unpacking for text display
def __text_objects(text, font):
    surface = font.render(text, True, BLACK)
    return surface, surface.get_rect()


# Unpacking the images required to display the controls in the splash screen
# If an incorrect player ID is used, an error will be raised
# (!) TODO: Resize the images for the buttons to 60x60/70x70 so that they fit better (!)
def load_controls_images(player):
    if player == 1:
        # Load player 1 images
        rotate_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_A.png')
        rotate_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_D.png')
        thrust = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_W.png')
        return rotate_left, rotate_right, thrust
    elif player == 2:
        # Load player 2 images
        move_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Left.png')
        move_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Right.png')
        shoot = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Space.png')
        cannon_left = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Down.png')
        cannon_right = pygame.image.load(
            'frames/keys/Keyboard & Mouse/Light/Keyboard_White_Arrow_Up.png')
        return move_left, move_right, shoot, cannon_left, cannon_right
    else:
        raise ValueError("Error when specifying player number.")


# Method used to display text
# It's used on multiple occasions that's why it's taken out as a separate method
# Args: screen -> pygame.display object
#       text -> string you want displayed
#       size -> the size of the string (different lengths need different size)
#       font -> name of the font
def display_text(screen, text, font, size):
    screen = screen.get_surface()
    width, height = screen.get_size()
    font = pygame.font.Font(font, size)
    surface, rect = __text_objects(text, font)
    rect.center = ((width / 2), (height / 4))
    screen.blit(surface, rect)
    pygame.display.update()


class SceneBase:
    def __init__(self):
        self.next = self
        # Fonts:
        self.font_arial_black = pygame.font.SysFont('Arial Black', 18)
        self.font_verdana = pygame.font.SysFont('Verdana', 35)
        self.font_arial_black_large = pygame.font.SysFont('Arial Black', 50)
        self.font_verily_mono = pygame.font.SysFont('Verily Serif Mono', 27)
        self.font_freesans_bold = pygame.font.SysFont("Freesans Bold", 35)

    # Using this method mainly for testing
    # The game logic will be implemented in the Update() method
    def ProcessInput(self, events, pressed_keys):
        print("(!) Override in child class (!)")

    def Update(self):
        print("(!) Override in child class (!)")

    def Render(self, screen):
        print("(!) Override in child class (!)")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.width = T_SCREEN_WIDTH
        self.height = T_SCREEN_HEIGHT

        # Start and Quit buttons
        self.menu_button = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 2, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Start')
        self.menu_button_2 = Button((self.width / 2 - (BUTTON_WIDTH / 2), self.height / 1.5, BUTTON_WIDTH,
                                     BUTTON_HEIGHT), RED, 'Quit')

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                self.SwitchToScene(SplashScene())

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

        # Update title
        title_update(title_surfaces, screen)


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

        self.draw_text(screen, "Game Controls", (splash_x + (splash_w/3),
                                                 splash_y), self.font_arial_black_large, (140, 123, 192))
        self.draw_text(screen, "Player 1: ", (splash_x + 100,
                                              splash_y + 100), self.font_verdana, (255, 255, 255))
        self.draw_text(screen, "Player 2: ", (splash_x + 450,
                                              splash_y + 100), self.font_verdana, (255, 255, 255))

        # Display the controls for Player 1 (controlling the ship)
        # on the splash screen

        screen.get_surface().blit(player1_thrust, (splash_x + 125, splash_y + 150))
        self.draw_text(screen, "Thruster On", (splash_x + 110,
                                               splash_y + 140), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(player1_left, (splash_x + 50, splash_y + 250))
        self.draw_text(screen, "Rotate Left", (splash_x + 35,
                                               splash_y + 240), self.font_freesans_bold, WHITE)

        screen.get_surface().blit(player1_right, (splash_x + 200, splash_y + 250))
        self.draw_text(screen, "Rotate Right", (splash_x + 190,
                                                splash_y + 240), self.font_freesans_bold, WHITE)

        # Display the controls for Player 2 (controlling the tank)
        # on the splash screen

        screen.get_surface().blit(player2_cannon_right, (splash_x + 475, splash_y + 150))
        self.draw_text(screen, "Cannon Right", (splash_x + 450,
                                                splash_y + 140), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_cannon_left, (splash_x + 475, splash_y + 350))
        self.draw_text(screen, "Cannon Right", (splash_x + 450,
                                                splash_y + 340), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_left, (splash_x + 375, splash_y + 250))
        self.draw_text(screen, "Move Left", (splash_x + 360,
                                             splash_y + 240), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_right, (splash_x + 575, splash_y + 250))
        self.draw_text(screen, "Move Right", (splash_x + 560,
                                              splash_y + 240), self.font_freesans_bold, WHITE)
        screen.get_surface().blit(player2_shoot, (splash_x + 475, splash_y + 450))
        self.draw_text(screen, "Shoot", (splash_x + 485,
                                         splash_y + 445), self.font_freesans_bold, WHITE)

        self.splash_button.update(screen.get_surface())
        pygame.display.update()

    @staticmethod
    def draw_text(screen, message, position, font, color=(0, 0, 0)):
        text = font.render(message, False, color)
        screen.get_surface().blit(text, position)


class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.end_time = 0
        self.start_time = 0
        self.screen_width = G_SCREEN_WIDTH
        self.screen_height = G_SCREEN_HEIGHT
        self.space = pymunk.Space()
        self.space.gravity = EARTH_GRAVITY
        self.terrain = self.random_terrain(self.space)
        self.borders()
        self.space.add(self.terrain)

        # Anti-spacecraft
        self.anti_spacecraft = AntiSpaceCraft()

        self.space.add(self.anti_spacecraft.wheel1_b, self.anti_spacecraft.wheel1_s)
        self.space.add(self.anti_spacecraft.wheel2_b, self.anti_spacecraft.wheel2_s)
        self.space.add(self.anti_spacecraft.chassis_b, self.anti_spacecraft.chassis_s)
        self.space.add(self.anti_spacecraft.cannon_b, self.anti_spacecraft.cannon_s)
        self.space.add(self.anti_spacecraft.missile_shape)
        self.space.add(self.anti_spacecraft.pin1, self.anti_spacecraft.pin2, self.anti_spacecraft.pin3,
                       self.anti_spacecraft.pin4, self.anti_spacecraft.pin5, self.anti_spacecraft.pin6)

        self.space.add(self.anti_spacecraft.pin8, self.anti_spacecraft.cannon_mt)

        self.spacecraft = Spacecraft((200, 500))
        self.space.add(self.spacecraft.body, self.spacecraft.shape)

    def ProcessInput(self, events, pressed_keys):

        # Arrow keys movement
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_RIGHT]:
            self.anti_spacecraft.force_right()
        if keys[pygame.K_LEFT]:
            self.anti_spacecraft.force_left()
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.anti_spacecraft.force = DEFAULT_FORCE

        if keys[pygame.K_DOWN]:
            self.anti_spacecraft.cannon_mt.rate = 2.5
        if keys[pygame.K_UP]:
            self.anti_spacecraft.cannon_mt.rate = -2.5
        if not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.anti_spacecraft.cannon_mt.rate = 0

        if keys[pygame.K_a]:
            self.spacecraft.rotate_left()
        if keys[pygame.K_d]:
            self.spacecraft.rotate_right()
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.spacecraft.body.angular_velocity = 0

        if keys[pygame.K_w]:
            self.spacecraft.move_up()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(WinScene())
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                self.SwitchToScene(LoseScene())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_time = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.end_time = pygame.time.get_ticks()
                self.anti_spacecraft.cannon_mt.rate = 0

                diff = self.end_time - self.start_time
                power = max(min(diff, 1000), 10) * 1.5
                impulse = power * Vec2d(1, 0)
                impulse.rotate(self.anti_spacecraft.missile_body.angle)

                self.anti_spacecraft.missile_body.apply_impulse_at_world_point\
                    (impulse, self.anti_spacecraft.missile_body.position)

                self.space.add(self.anti_spacecraft.missile_body)
                self.anti_spacecraft.flying_missiles.append(self.anti_spacecraft.missile_body)

                self.anti_spacecraft.missile_body, self.anti_spacecraft.missile_shape = self.anti_spacecraft.create_missile()
                self.space.add(self.anti_spacecraft.missile_shape)

            # Position the missile
            self.anti_spacecraft.missile_body.position = self.anti_spacecraft.cannon_b.position + Vec2d(
                self.anti_spacecraft.cannon_s.radius - 55, 0).rotated(self.anti_spacecraft.cannon_b.angle)
            self.anti_spacecraft.missile_body.angle = self.anti_spacecraft.cannon_b.angle + math.pi

            for missile in self.anti_spacecraft.flying_missiles:
                drag_constant = 0.0002

                pointing_direction = Vec2d(1, 0).rotated(missile.angle)
                flight_direction = Vec2d(missile.velocity)
                flight_speed = flight_direction.normalize_return_length()
                dot = flight_direction.dot(pointing_direction)

                drag_force_magnitude = (1 - abs(dot)) * flight_speed ** 2 * drag_constant * missile.mass
                missile_tail_position = Vec2d(-50, 0).rotated(missile.angle)
                missile.apply_impulse_at_world_point(drag_force_magnitude * -flight_direction, missile.position)

                missile.angular_velocity *= 0.5

    def Update(self):
        pass

    @staticmethod
    def random_terrain(space):
        # Tuples of points where new segment will be added to form the terrain
        terrain = []
        points = [(i, random.randint(G_SCREEN_HEIGHT//20, G_SCREEN_HEIGHT//10))
                  for i in range(0, G_SCREEN_WIDTH + SEGMENT_LENGTH, SEGMENT_LENGTH)]

        # Loop to add the segments to the space
        for i in range(1, len(points)):
            floor = pymunk.Segment(space.static_body, (points[i - 1][0], points[i - 1][1]),
                                   (points[i][0], points[i][1]), TERRAIN_THICKNESS)
            floor.friction = TERRAIN_FRICTION
            floor.filter = pymunk.ShapeFilter(group=0)
            terrain.append(floor)
        return terrain

    def borders(self):
        # Screen borders
        border_left = pymunk.Segment(self.space.static_body, (0, 0), (0, self.screen_height), 1)
        border_right = pymunk.Segment(self.space.static_body, (self.screen_width, 0), (self.screen_width,
                                                                                       self.screen_height), 1)
        border_top = pymunk.Segment(self.space.static_body, (0, self.screen_height), (self.screen_width,
                                                                                      self.screen_height), 1)
        self.space.add(border_left, border_right, border_top)

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().fill(BLUE)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            diff = current_time - self.start_time
            power = max(min(diff, 1000), 10)
            h = power / 2
            pygame.draw.line(screen.get_surface(), pygame.color.THECOLORS["red"], (30, 550), (30, 550 - h), 10)

        self.spacecraft.update()
        self.space.step(1. / FPS)
        draw_options = pymunk.pygame_util.DrawOptions(screen.get_surface())
        self.space.debug_draw(draw_options)
        self.anti_spacecraft.apply_force()


class WinScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((800, 600))
        screen.get_surface().fill(GREEN)
        display_text(screen, "Congratulations! You have won!", 'freesansbold.ttf', 50)


class LoseScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((800, 600))
        screen.get_surface().fill(RED)
        display_text(screen, "Too bad! You have lost!", 'freesansbold.ttf', 45)