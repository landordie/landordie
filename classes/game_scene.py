import math
import random
import pymunk
from pymunk import pygame_util, Vec2d
from classes.landing_pad import LandingPad
from classes.spacecraft import Spacecraft, flipy
from .scene_base import *
from .result_scene import ResultScene
from .anti_spacecraft import AntiSpaceCraft
import constants
from .controls import Controls
from pygame.time import Clock as GameClock


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

        # Add the terrain
        self.terrain = self.random_terrain(self.space)
        self.borders()
        self.space.add(self.terrain)

        self.background = pg.image.load("frames/backgr1.jpg")
        self.release_time = 0  # Used for making the cooldown function of the shooter. Between 0 and 120 frames
        self.landing_pad = LandingPad()
        self.ctrls = Controls.get_controls()

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

        self.space.add(self.spacecraft.body, self.spacecraft.shape)

        # self.crash_handler = self.space.add_collision_handler(0, 3)
        # self.crash_handler.data["spacecraft_land"] = self.spacecraft.body
        # self.crash_handler.post_solve = self.post_solve_crashed

    def post_solve_adjust_scores(self, arbiter):
        if arbiter.total_impulse.length > 100:
            self.player1_pts += 10
            self.spacecraft.receive_damage(20)

    # def post_solve_crashed(self, arbiter, space, data):
    #     """ Set the spacecraft score to 50 only if it is a smooth landing. """
    #     if self.spacecraft.body.velocity.length < 10 and not self.spacecraft.crashed:
    #         self.player2_pts = 50
    #         self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))
    #     # set spacecraft crashed attribute to True when it collides too fast
    #     elif self.spacecraft.body.velocity.length > 100:
    #         self.display_crash_text = True
    #         self.spacecraft.crashed = True

    def pause_game(self, msg_type, screen):
        """ The method pauses the game after the player crashes and displays a message, till a key is pressed """
        msg = ''

        if msg_type == 'landed':
            msg = self.font_warning.render("Successful Landing!", False, (13, 109, 24))
        elif msg_type == 'crashed':
            msg = self.font_warning.render("You Have Crashed!", False, (255, 0, 6))

        screen.blit(msg, (330, 375))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Checks if the user wants to quit tha game by clicking on the "X" button
                    return True
                if event.type == pygame.KEYDOWN:
                    # Checks if any key is pressed - Resumes the game
                    return False

            pygame.display.update()
            GameClock().tick(FPS)

    def ProcessInput(self, events, pressed_keys):

        # Arrow keys movement
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[CONTROL_DICT[self.ctrls[5]]]:
            self.anti_spacecraft.force_right()
        elif keys[CONTROL_DICT[self.ctrls[3]]]:
            self.anti_spacecraft.force_left()
        else:
            self.anti_spacecraft.force = DEFAULT_FORCE

        if keys[pygame.K_DOWN] and self.anti_spacecraft.cannon_b.angle < 0:
            self.anti_spacecraft.cannon_mt.rate = 2
        elif keys[pygame.K_UP] and self.anti_spacecraft.cannon_b.angle >= -math.pi:
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_time = pygame.time.get_ticks()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.spacecraft.gravity_control_system()

            if self.release_time <= 0:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.end_time = pygame.time.get_ticks()
                    self.anti_spacecraft.cannon_mt.rate = 0

                    diff = self.end_time - self.start_time
                    power = max(min(diff, 1000), 10)
                    impulse = power * Vec2d(1, 0)
                    impulse.rotate(self.anti_spacecraft.missile_body.angle)
                    self.release_time = 120

                    self.anti_spacecraft.missile_body.apply_impulse_at_world_point\
                        (impulse, self.anti_spacecraft.missile_body.position)

                    self.space.add(self.anti_spacecraft.missile_body)
                    self.anti_spacecraft.flying_missiles.append(self.anti_spacecraft.missile_body)

                    self.anti_spacecraft.missile_body, self.anti_spacecraft.missile_shape = \
                        self.anti_spacecraft.create_missile()
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
        points = [(i, random.randint(constants.G_SCREEN_HEIGHT//45, constants.G_SCREEN_HEIGHT//7))
                  for i in range(0, constants.G_SCREEN_WIDTH + SEGMENT_LENGTH, SEGMENT_LENGTH)]

        # Loop to add the segments to the space
        for i in range(1, len(points)):
            floor = pymunk.Segment(space.static_body, (points[i - 1][0], points[i - 1][1]),
                                   (points[i][0], points[i][1]), TERRAIN_THICKNESS//3)
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
        border_bottom = pymunk.Segment(self.space.static_body, (0, 0), (self.screen_width, 0), 75)
        border_bottom.friction = TERRAIN_FRICTION
        border_top.collision_type = 4
        self.space.add(border_left, border_right, border_top, border_bottom)

    def Render(self, screen):
        display = screen.get_surface()
        screen.set_mode((self.screen_width, self.screen_height))
        display.blit(self.background, (0, 0))

        # Show the missile ###########################################################

        # Landing pad Sprite
        display.blit(self.landing_pad.image, self.landing_pad.rect)

        # Space craft Sprite
        display.blit(self.spacecraft.rotatedImg, self.spacecraft.rect)

        self.space.step(1. / FPS)
        draw_options = pymunk.pygame_util.DrawOptions(display)
        self.space.debug_draw(draw_options)

        if self.release_time > 0:
            self.release_time -= 1
            self.start_time = pygame.time.get_ticks()
            cooldown = max(self.release_time, 0) * 1.5

            pygame.draw.line(display, pygame.color.THECOLORS["blue"], (1125, 750), (1125, 750 - cooldown), 10)

        if pygame.key.get_pressed()[pygame.K_SPACE] and self.release_time <= 0:
            # Position the missile
            self.anti_spacecraft.missile_body.position = self.anti_spacecraft.cannon_b.position + Vec2d(
                self.anti_spacecraft.cannon_s.radius - 37, 0).rotated(self.anti_spacecraft.cannon_b.angle)

            # TODO attach missile sprite
            # self.anti_spacecraft.m_rect = flipy(self.anti_spacecraft.cannon_b.position + Vec2d(
            #     self.anti_spacecraft.cannon_s.radius - 37, 0).rotated(self.anti_spacecraft.cannon_b.angle))
            self.anti_spacecraft.m_rect.center = flipy(self.anti_spacecraft.missile_body.position)

            # TODO fix rotation
            self.anti_spacecraft.rotated_missile = pg.transform.rotate(self.anti_spacecraft.missile, math.degrees(self.anti_spacecraft.cannon_b.angle))

            # Pymunk missile
            self.anti_spacecraft.missile_body.angle = self.anti_spacecraft.cannon_b.angle + math.pi

            display.blit(self.anti_spacecraft.rotated_missile, self.anti_spacecraft.m_rect)
            current_time = pygame.time.get_ticks()
            diff = current_time - self.start_time
            power = max(min(diff, 750), 0)
            h = power / 4
            pygame.draw.line(display, pygame.color.THECOLORS["red"], (1150, 750), (1150, 750 - h), 10)
        
        # Anti-Spacecraft fuel bar
        fuel = max(self.anti_spacecraft.fuel, 0)
        pygame.draw.line(display, RED, flipy((self.anti_spacecraft.chassis_b.position - (80, 45))),
                         flipy((self.anti_spacecraft.chassis_b.position[0] + 87,
                                self.anti_spacecraft.chassis_b.position[1] - 45)), 10)  # Red bar underneath
        pygame.draw.line(display, GREEN, flipy((self.anti_spacecraft.chassis_b.position - (80, 45))),
                         flipy((self.anti_spacecraft.chassis_b.position[0] - 79 + fuel / 3,
                                self.anti_spacecraft.chassis_b.position[1] - 45)), 10)  # FUEL (green bar)

        #self.spacecraft.fall_down()
        if pygame.sprite.collide_mask(self.landing_pad, self.spacecraft):
            if self.landing_pad.check_for_landing_attempt(self.spacecraft):
                paused = self.pause_game('landed', display)
                if paused:
                    self.Terminate()
                else:
                    self.player1_pts += 50
                    self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

        # image draw
        p = self.spacecraft.body.position
        p = flipy(p)

        # we need to rotate 180 degrees because of the y coordinate flip
        self.spacecraft.rotation_angle = math.degrees(self.spacecraft.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(self.spacecraft.image, self.spacecraft.rotation_angle)

        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset

        display.blit(rotated_logo_img, p)

        # debug draw
        ps = [p.rotated(self.spacecraft.body.angle) + self.spacecraft.body.position for p in self.spacecraft.shape.get_vertices()]
        ps = [(p.x, (-p.y + 800)) for p in ps]
        ps += [ps[0]]
        pygame.draw.lines(display, RED, False, ps, 1)

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

        # Move the Anti-Spacecraft if buttons pressed
        self.anti_spacecraft.apply_force()
