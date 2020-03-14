import math
import random
import pymunk
from pymunk import pygame_util, Vec2d
from classes.landing_pad import LandingPad
from classes.spacecraft import Spacecraft
from .scene_base import *
from .result_scene import ResultScene
from .anti_spacecraft import AntiSpaceCraft
from .missile import Missile
import constants
from .controls import Controls
from pygame.time import Clock as GameClock
from .star_field import StarField


# (!) Note (!) : Every time we use self.screen_height and G_SCREEN_WIDTH we have to type "constants." before so it works

class GameScene(SceneBase):

    border_sf = pymunk.ShapeFilter(group=2)

    def __init__(self):

        SceneBase.__init__(self)

        # Initialize the environment and all the objects except the players:
        #        terrain, borders, landing pad, stars, background, etc.
        self.space = pymunk.Space()  # Pymunk Space - the active game environment
        self.space.gravity = EARTH_GRAVITY
        self.borders()
        self.terrain = self.random_terrain()
        self.space.add(self.terrain)
        self.landing_pad = LandingPad(self.screen_width - 100, self.screen_height)
        self.ctrls = Controls.get_controls()

        self.star_field = StarField(self.screen_width, self.screen_height)
        self.missile = Missile()  # Missile object
        self.background = pg.image.load("frames/splash_BG.jpg")
        self.release_time = 0  # Used for making the cooldown function of the shooter. Between 0 and 120 frames

        # Anti-spacecraft
        self.anti_spacecraft = AntiSpaceCraft()

        # Spacecraft
        self.spacecraft = Spacecraft(self.screen_width)
        # Setting the spacecraft collision type so the collision handler can check for it
        self.spacecraft.shape.collision_type = 2

        # Collision handler looks for shapes with collision type 2 and 3
        # 2 -> spacecraft which is set further down in the constructor
        # 3 -> missile which is set in the anti_spacecraft.create_missile() method
        # 4 -> wall segments
        self.handler = self.space.add_collision_handler(2, 3)
        self.wall_handler = self.space.add_collision_handler(4, 3)

        # We must set the 4 callbacks so the handler works properly
        # Even though we're just using the .begin one
        self.start_collision_handlers()
        # Add spacecraft and anti-spacecraft pymunk representations to space
        self.add_objects_to_space()

        self.player1_pts = 0
        self.player2_pts = 0
        self.end_time = 0
        self.start_time = 0
        self.check = True
        self.collision = False

    def ProcessInput(self, events, pressed_keys):

        # Arrow keys movement
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[CONTROL_DICT[self.ctrls[5]]]:
            self.anti_spacecraft.force_right()
        elif keys[CONTROL_DICT[self.ctrls[3]]]:
            self.anti_spacecraft.force_left()
        else:
            self.anti_spacecraft.force = DEFAULT_FORCE

        if keys[CONTROL_DICT[self.ctrls[6]]] and self.anti_spacecraft.cannon_b.angle < 0:
            self.anti_spacecraft.cannon_mt.rate = 2
        elif keys[CONTROL_DICT[self.ctrls[4]]] and self.anti_spacecraft.cannon_b.angle >= -math.pi:
            self.anti_spacecraft.cannon_mt.rate = -2
        else:
            self.anti_spacecraft.cannon_mt.rate = 0

        if not self.spacecraft.crashed:
            # Rotate spacecraft (in radians)
            if keys[CONTROL_DICT[self.ctrls[0]]]:
                self.spacecraft.body.angle += math.radians(2)
            if keys[CONTROL_DICT[self.ctrls[2]]]:
                self.spacecraft.body.angle -= math.radians(2)
            if keys[CONTROL_DICT[self.ctrls[1]]]:
                self.spacecraft.apply_thrust()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

            if self.release_time <= 0:
                if pygame.key.get_pressed()[pygame.K_SPACE] and self.check:
                    # Create new missile and add it to the space
                    self.anti_spacecraft.missile_body, self.anti_spacecraft.missile_shape = \
                        self.anti_spacecraft.create_missile((-1000, -1232))
                    self.space.add(self.anti_spacecraft.missile_shape)

                    self.start_time = pygame.time.get_ticks()
                    self.collision = False
                    self.check = False

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.end_time = pygame.time.get_ticks()
                    self.anti_spacecraft.cannon_mt.rate = 0

                    diff = self.end_time - self.start_time
                    power = max(min(diff, 1000), 10)
                    impulse = power * Vec2d(1, 0)
                    impulse.rotate(self.anti_spacecraft.missile_body.angle)

                    # Reset cool down
                    self.release_time = 120
                    self.check = True

                    # Apply force to the missile (launch the missile)
                    self.anti_spacecraft.missile_body.apply_impulse_at_world_point \
                        (impulse, self.anti_spacecraft.missile_body.position)

                    # Add the missile body to the space
                    self.space.add(self.anti_spacecraft.missile_body)

                    # Add the missile body to the flying missiles
                    self.anti_spacecraft.missile_shape.collision_type = 3
                    self.anti_spacecraft.flying_missiles.append(self.anti_spacecraft.missile_body)

            # Apply gravitational effects to all the current flying missiles
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

    def Render(self, screen):
        display = screen.get_surface()
        screen.set_mode((self.screen_width, self.screen_height))
        display.blit(self.background, (0, 0))
        self.star_field.draw_stars(display)

        # Display pymunk bodies
        self.space.step(1. / FPS)
        draw_options = pymunk.pygame_util.DrawOptions(display)
        self.space.debug_draw(draw_options)

        # Landing pad Sprite
        display.blit(self.landing_pad.image, self.landing_pad.rect)

        if self.release_time > 0:
            self.release_time -= 1
            self.start_time = pygame.time.get_ticks()
            cooldown = max(self.release_time, 0) * 1.5

            pygame.draw.line(display, pygame.color.THECOLORS["blue"], (1125, 750), (1125, 750 - cooldown), 10)
        else:
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.anti_spacecraft.missile_body:
                # Position the missile
                self.anti_spacecraft.missile_body.position = self.anti_spacecraft.cannon_b.position + Vec2d(
                    self.anti_spacecraft.cannon_s.radius - 37, 0).rotated(self.anti_spacecraft.cannon_b.angle)

                # Pymunk missile
                self.anti_spacecraft.missile_body.angle = self.anti_spacecraft.cannon_b.angle + math.pi

                current_time = pygame.time.get_ticks()
                diff = current_time - self.start_time
                power = max(min(diff, 750), 0)
                h = power / 4
                pygame.draw.line(display, pygame.color.THECOLORS["red"], (1150, 750), (1150, 750 - h), 10)

        """
        Missile sprite blit
        """
        if self.anti_spacecraft.missile_shape:
            m, missile_img = self.missile.get_attachment_coordinates(self.anti_spacecraft.missile_body, self.screen_height)
            if not self.collision:
                display.blit(missile_img, m)

        ###########################
        # Anti-Spacecraft fuel bar
        ##########################
        fuel = max(self.anti_spacecraft.fuel, 0)
        pygame.draw.line(display, RED, flipy((self.anti_spacecraft.chassis_b.position - (80, 45)), self.screen_height),
                         flipy((self.anti_spacecraft.chassis_b.position[0] + 87,
                                self.anti_spacecraft.chassis_b.position[1] - 45), self.screen_height), 10)  # Red bar underneath
        pygame.draw.line(display, GREEN, flipy((self.anti_spacecraft.chassis_b.position - (80, 45)), self.screen_height),
                         flipy((self.anti_spacecraft.chassis_b.position[0] - 79 + fuel / 3,
                                self.anti_spacecraft.chassis_b.position[1] - 45), self.screen_height), 10)  # FUEL (green bar)

        ###########################
        # Spacecraft health bar
        ##########################
        pygame.draw.line(display, WHITE, flipy((self.spacecraft.body.position - (80, 45)), self.screen_height),
                         flipy((self.spacecraft.body.position[0] + 75,
                                self.spacecraft.body.position[1] - 45), self.screen_height), 10)  # Red bar underneath
        # Changes colors
        self.spacecraft.health_bar(display, self.screen_height)

        # Attach the spacecraft sprite to the pymunk shape
        p, sc_sprite = self.spacecraft.get_attachment_coordinates(self.spacecraft.body, self.screen_height)
        self.spacecraft.rect = sc_sprite.get_rect(left=p[0], top=p[1])
        display.blit(sc_sprite, self.spacecraft.rect)

        p, rotated_cannon_img = self.anti_spacecraft.cannon_sprite.get_attachment_coordinates(self.anti_spacecraft.cannon_b, self.screen_height)
        if 0 < abs(math.degrees(self.anti_spacecraft.cannon_b.angle)) < 144:
            # Helps adjusting the alignment b/w cannon body and cannon sprite
            p[0] += 5
        if 145 < abs(math.degrees(self.anti_spacecraft.cannon_b.angle)) < 184:
            # Helps adjusting the alignment b/w cannon body and cannon sprite
            p[0] += 7
        self.anti_spacecraft.cannon_sprite.rect = rotated_cannon_img.get_rect(left=p[0], top=p[1])
        display.blit(rotated_cannon_img, self.anti_spacecraft.cannon_sprite.rect)

        p, rotated_body_img = self.anti_spacecraft.body_sprite.get_attachment_coordinates(self.anti_spacecraft.chassis_b, self.screen_height)
        self.anti_spacecraft.body_sprite.rect = rotated_body_img.get_rect(left=p[0], top=p[1]-15)
        display.blit(rotated_body_img, self.anti_spacecraft.body_sprite.rect)

        # Move the Anti-Spacecraft if buttons pressed
        self.anti_spacecraft.apply_force()

        if self.spacecraft.health == 0:
            paused = self.pause_game('no HP', display)
            if paused:
                self.Terminate()
            else:
                self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

        if pygame.sprite.collide_mask(self.landing_pad, self.spacecraft):
            if self.landing_pad.check_for_landing_attempt(self.spacecraft):
                paused = self.pause_game('landed', display)
                if paused:
                    self.Terminate()
                else:
                    self.player1_pts += 50
                    self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

    # The following 4 methods(callbacks) are required for the collision handler to work
    # The only one we are using is the collision_begin
    # It happens at the exact moment a missile and the spacecraft collide
    def post_solve_adjust_scores(self, arbiter, space, data):
        pass

    def wall_collision_begin(self, arbiter, space, data):
        self.space.remove(self.anti_spacecraft.missile_body)
        self.space.remove(self.anti_spacecraft.missile_shape)
        self.collision = True

        return True

    def add_objects_to_space(self):
        # Anti-spacecraft Parts (represent the whole vehicle)
        self.space.add(self.anti_spacecraft.wheel1_b, self.anti_spacecraft.wheel1_s)
        self.space.add(self.anti_spacecraft.wheel2_b, self.anti_spacecraft.wheel2_s)
        self.space.add(self.anti_spacecraft.chassis_b, self.anti_spacecraft.chassis_s)
        self.space.add(self.anti_spacecraft.cannon_b, self.anti_spacecraft.cannon_s)
        self.space.add(self.anti_spacecraft.pin1, self.anti_spacecraft.pin2, self.anti_spacecraft.pin3,
                       self.anti_spacecraft.pin4, self.anti_spacecraft.pin5, self.anti_spacecraft.pin6)
        self.space.add(self.anti_spacecraft.pin8, self.anti_spacecraft.cannon_mt)

        # Spacecraft object
        self.space.add(self.spacecraft.body, self.spacecraft.shape)

    def start_collision_handlers(self):
        self.wall_handler.begin = self.wall_collision_begin
        self.handler.begin = self.collision_begin
        self.handler.pre_solve = self.collision_pre
        self.handler.post_solve = self.post_solve_adjust_scores
        self.handler.separate = self.collision_separate
        self.wall_handler.pre_solve = self.collision_pre
        self.wall_handler.post_solve = self.post_solve_adjust_scores
        self.wall_handler.separate = self.collision_separate

    def collision_begin(self, arbiter, space, data):
        self.spacecraft.receive_damage(20)
        self.player2_pts += 10
        self.collision = True

        self.space.remove(self.anti_spacecraft.missile_body)
        self.space.remove(self.anti_spacecraft.missile_shape)

        return True

    def collision_pre(self, arbiter, space, data):
        return True

    def collision_separate(self, arbiter, space, data):
        pass

    def pause_game(self, msg_type, screen):
        """ The method pauses the game after the player crashes and displays a message, till a key is pressed """
        msg = ''

        if msg_type == 'landed':
            msg = self.font_warning.render("Successful Landing!", False, (13, 109, 24))
        elif msg_type == 'crashed':
            msg = self.font_warning.render("The spacecraft has crashed!", False, (255, 0, 6))
        elif msg_type == 'no HP':
            msg = self.font_warning.render("The spacecraft has been destroyed (0 HP left)", False, (255, 0, 6))

        msg_rect = msg.get_rect()
        msg_rect.center = ((self.screen_width/2), (self.screen_height/2.3))
        instructions = self.font_warning.render("Game ended. Press ENTER to see results.", False, CYAN)
        instructions_rect = instructions.get_rect()
        instructions_rect.center = ((self.screen_width/2), (self.screen_height/2))

        screen.blit(msg, msg_rect)
        screen.blit(instructions, instructions_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Checks if the user wants to quit tha game by clicking on the "X" button
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Checks if any key is pressed - Resumes the game
                    return False

            pygame.display.update()
            GameClock().tick(FPS)

    def random_terrain(self):
        """
        Create a random terrain from pymunk Segments
        :return: random terrain
        """
        # Tuples of points where new segment will be added to form the terrain
        terrain = []
        points = [(i, random.randint(self.screen_height // 20, self.screen_height // 7))
                  for i in range(0, self.screen_width + SEGMENT_LENGTH, SEGMENT_LENGTH)]

        # Loop to add the segments to the space
        for i in range(1, len(points)):
            floor = pymunk.Segment(self.space.static_body, (points[i - 1][0], points[i - 1][1]),
                                   (points[i][0], points[i][1]), TERRAIN_THICKNESS)
            floor.friction = TERRAIN_FRICTION
            floor.filter = pymunk.ShapeFilter(group=0)
            floor.collision_type = 4
            floor.filter = GameScene.border_sf
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
        border_bottom.color = DARK_GREY

        border_top.filter = GameScene.border_sf
        border_bottom.filter = GameScene.border_sf
        border_right.filter = GameScene.border_sf
        border_left.filter = GameScene.border_sf

        border_top.collision_type = 4
        border_left.collision_type = 4
        border_right.collision_type = 4
        border_bottom.collision_type = 4
        self.space.add(border_left, border_right, border_top, border_bottom)
