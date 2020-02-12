import math
import random
import pymunk
from pymunk import pygame_util, Vec2d
from classes.spacecraft import Spacecraft
from .scene_base import *
from .result_scene import ResultScene
from .anti_spacecraft import AntiSpaceCraft
import constants
from time import clock as game_clock

# (!) Note (!) : Every time we use G_SCREEN_HEIGHT and G_SCREEN_WIDTH we have to type "constants." before so it works


class GameScene(SceneBase):

    def __init__(self):
        SceneBase.__init__(self)
        self.player2_pts = 0
        self.display_crash_text = False
        self.player1_pts = 0
        self.end_time = 0
        self.start_time = 0
        self.screen_width = constants.G_SCREEN_WIDTH
        self.screen_height = constants.G_SCREEN_HEIGHT
        self.space = pymunk.Space()
        self.space.gravity = EARTH_GRAVITY
        self.terrain = self.random_terrain(self.space)
        self.borders()
        self.space.add(self.terrain)
        self.background = pg.image.load("frames/backgr1.jpg")
        self.release_time = 0  # Used for making the cooldown function of the shooter. Between 0 and 120 frames

        # Anti-spacecraft
        self.anti_spacecraft = AntiSpaceCraft()
        self.handler = self.space.add_collision_handler(2, 3)
        self.handler.data["flying_missiles"] = self.anti_spacecraft.flying_missiles
        self.handler.post_solve = self.post_solve_adjust_scores

        self.space.add(self.anti_spacecraft.wheel1_b, self.anti_spacecraft.wheel1_s)
        self.space.add(self.anti_spacecraft.wheel2_b, self.anti_spacecraft.wheel2_s)
        self.space.add(self.anti_spacecraft.chassis_b, self.anti_spacecraft.chassis_s)
        self.space.add(self.anti_spacecraft.cannon_b, self.anti_spacecraft.cannon_s)
        self.space.add(self.anti_spacecraft.missile_shape)
        self.space.add(self.anti_spacecraft.pin1, self.anti_spacecraft.pin2, self.anti_spacecraft.pin3,
                       self.anti_spacecraft.pin4, self.anti_spacecraft.pin5, self.anti_spacecraft.pin6)

        self.space.add(self.anti_spacecraft.pin8, self.anti_spacecraft.cannon_mt)

        self.spacecraft = Spacecraft(constants.G_SCREEN_WIDTH)
        # self.space.add(self.spacecraft.body, self.spacecraft.shape)

        # self.crash_handler = self.space.add_collision_handler(0, 3)
        # self.crash_handler.data["spacecraft_land"] = self.spacecraft.body
        # self.crash_handler.post_solve = self.post_solve_crashed

    def post_solve_adjust_scores(self, arbiter, space, data):
        if arbiter.total_impulse.length > 100:
            self.player1_pts += 10

    def post_solve_crashed(self, arbiter, space, data):
        """ Set the spacecraft score to 50 only if it is a smooth landing. """
        if self.spacecraft.body.velocity.length < 10 and not self.spacecraft.crashed:
            self.player2_pts = 50
            self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))
        # set spacecraft crashed attribute to True when it collides too fast
        elif self.spacecraft.body.velocity.length > 100:
            self.display_crash_text = True
            self.spacecraft.crashed = True

    def ProcessInput(self, events, pressed_keys):

        # Arrow keys movement
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_RIGHT]:
            self.anti_spacecraft.force_right()
        elif keys[pygame.K_LEFT]:
            self.anti_spacecraft.force_left()
        else:
            self.anti_spacecraft.force = DEFAULT_FORCE

        if keys[pygame.K_DOWN] and self.anti_spacecraft.cannon_b.angle < 0:
            self.anti_spacecraft.cannon_mt.rate = 2
        elif keys[pygame.K_UP]:
            self.anti_spacecraft.cannon_mt.rate = -2
        else:
            self.anti_spacecraft.cannon_mt.rate = 0

        if not self.spacecraft.crashed:
            if keys[pygame.K_a]:
                self.spacecraft.rotate("left")
            elif keys[pygame.K_d]:
                self.spacecraft.rotate("right")
            elif keys[pygame.K_w]:
                self.spacecraft.active_engines = True
                self.spacecraft.activate_engines()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.release_time <= 0:
                    self.start_time = pygame.time.get_ticks()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.spacecraft.gravity_control_system()
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if self.release_time <= 0:
                    self.release_time = 120
                self.end_time = pygame.time.get_ticks()
                self.anti_spacecraft.cannon_mt.rate = 0

                diff = self.end_time - self.start_time
                power = max(min(diff, 1000), 10)
                impulse = power * Vec2d(1, 0)
                impulse.rotate(self.anti_spacecraft.missile_body.angle)

                self.anti_spacecraft.missile_body.apply_impulse_at_world_point\
                    (impulse, self.anti_spacecraft.missile_body.position)

                self.space.add(self.anti_spacecraft.missile_body)
                self.anti_spacecraft.flying_missiles.append(self.anti_spacecraft.missile_body)

                self.anti_spacecraft.missile_body, self.anti_spacecraft.missile_shape = self.anti_spacecraft.create_missile()
                self.space.add(self.anti_spacecraft.missile_shape)

            for missile in self.anti_spacecraft.flying_missiles:
                drag_constant = 0.0002

                pointing_direction = Vec2d(1, 0).rotated(missile.angle)
                flight_direction = Vec2d(missile.velocity)
                flight_speed = flight_direction.normalize_return_length()
                dot = flight_direction.dot(pointing_direction)

                drag_force_magnitude = (1 - abs(dot)) * flight_speed ** 2 * drag_constant * missile.mass
                missile.apply_impulse_at_world_point(drag_force_magnitude * -flight_direction, missile.position)

                missile.angular_velocity *= 0.5

    def Update(self):
        pass

    @staticmethod
    def random_terrain(space):
        # Tuples of points where new segment will be added to form the terrain
        terrain = []
        points = [(i, random.randint(constants.G_SCREEN_WIDTH//20, constants.G_SCREEN_HEIGHT//10))
                  for i in range(0, constants.G_SCREEN_WIDTH + SEGMENT_LENGTH, SEGMENT_LENGTH)]

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
        border_left = pymunk.Segment(self.space.static_body, (0, 0), (0, self.screen_height), 10)
        border_right = pymunk.Segment(self.space.static_body, (self.screen_width, 0), (self.screen_width,
                                                                                       self.screen_height), 10)
        border_top = pymunk.Segment(self.space.static_body, (0, self.screen_height), (self.screen_width,
                                                                                      self.screen_height), 10)
        border_top.collision_type = 4
        self.space.add(border_left, border_right, border_top)

    def Render(self, screen):
        self.release_time -= 1
        # The game scene is just a blank blue screen
        display = screen.get_surface()
        screen.set_mode((self.screen_width, self.screen_height))
        display.blit(self.background, (0, 0))

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.release_time <= 0:
            # self.release_time = game_clock()
            # if self.release_time < game_clock():
            # Position the missile
            self.anti_spacecraft.missile_body.position = self.anti_spacecraft.cannon_b.position + Vec2d(
                self.anti_spacecraft.cannon_s.radius - 37, 0).rotated(self.anti_spacecraft.cannon_b.angle)
            self.anti_spacecraft.missile_body.angle = self.anti_spacecraft.cannon_b.angle + math.pi
            current_time = pygame.time.get_ticks()
            diff = current_time - self.start_time
            power = max(min(diff, 1000), 10)
            h = power / 2
            pygame.draw.line(display, pygame.color.THECOLORS["red"], (30, 550), (30, 550 - h), 10)

        display.blit(self.spacecraft.rotatedImg, self.spacecraft.rect)

        self.spacecraft.fall_down()

        self.space.step(1. / FPS)
        draw_options = pymunk.pygame_util.DrawOptions(display)
        self.space.debug_draw(draw_options)
        if self.display_crash_text:
            text = self.font_warning.render("SPACECRAFT MALFUNCTION!!!", True, RED)
            text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 3))
            display.blit(text, text_rect)
        gravity_control_msg = self.font_freesans_bold.render("Gravity Control System: ", True, WHITE)
        display.blit(gravity_control_msg, gravity_control_msg.get_rect(center=(170, 30)))
        on, off = self.font_freesans_bold.render("ON", True, RED), self.font_freesans_bold.render("OFF", True, RED)
        w, h = gravity_control_msg.get_rect().center
        if self.spacecraft.counter_gravity:
            display.blit(on, on.get_rect(center=(w+185, h+20)))
        else:
            display.blit(off, off.get_rect(center=(w+190, h+20)))


        self.anti_spacecraft.apply_force()
