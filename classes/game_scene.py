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
from .controls import Controls
from pygame.time import Clock as GameClock
from .star_field import StarField


# (!) Note (!) : Every time we use self.screen_height and G_SCREEN_WIDTH we have to type "constants." before so it works

class GameScene(SceneBase):
    # Creates pymunk shape filter object which enables objects to pass through each other, do not collide
    border_sf = pymunk.ShapeFilter(group=2)

    def __init__(self):
        """This method initializes the Game Scene class. It is responsible for controlling the gameplay.
        Here all the game objects are initialized and used in one combined environment:
            * the first part is the pygame environment where all the sprites(images) are managed. This environment
              also displays the text and is responsible for opening and closing new windows, checking button clicks
              and event occurrences.

            * the second one is the pymunk space object which represents our physical realistic world. It creates and
              handles all the bodies and shapes standing behind the pygame sprites. All the physical forces in the
              pymunk space act on the bodies of the objects and they then determine what tha behaviour of the sprites
              will be.
        That way we can use the physics engine behind pymunk (chipmunk) together with the images, surfaces and user-
        input-handlers provided by pygame.
        """
        SceneBase.__init__(self)

        # Initialize the environment and all the objects except the players:
        #        terrain, borders, landing pad, stars, background, etc.
        self.space = pymunk.Space()  # Pymunk Space - the active game environment
        self.space.gravity = EARTH_GRAVITY
        self.borders()
        self.terrain = self.random_terrain()
        self.space.add(self.terrain)
        self.landing_pad = LandingPad(self.screen_width - 100, self.screen_height)
        self.pymunk_landing_pad = pymunk.Segment(self.space.static_body, flipy((self.landing_pad.rect.left + 14,
                                                                                self.landing_pad.rect.top + 16),
                                                                               self.screen_height),
                                                 flipy((self.landing_pad.rect.right - 14,
                                                        self.landing_pad.rect.top + 16), self.screen_height), 5)
        self.ctrls = Controls.get_controls()

        self.star_field = StarField(self.screen_width, self.screen_height)
        self.background = pg.image.load("frames/splash_BG.jpg")
        self.release_time = 0  # Used for making the cooldown function of the shooter. Between 0 and 120 frames

        # Anti-spacecraft
        self.anti_spacecraft = AntiSpaceCraft()

        # Spacecraft
        self.spacecraft = Spacecraft(self.screen_width)

        # Collision handler looks for shapes with collision type 2 and 3
        # 2 -> spacecraft which is set further down in the constructor
        # 3 -> missile which is set in the anti_spacecraft.create_missile() method
        # 4 -> wall segments
        self.missile_and_spacecraft_handler = self.space.add_collision_handler(2, 3)
        self.missile_and_terrain = self.space.add_collision_handler(4, 3)
        self.spacecraft_and_terrain_handler = self.space.add_collision_handler(2, 4)

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

            if event.type == pygame.KEYUP and event.key == CONTROL_DICT[self.ctrls[1]]:
                self.spacecraft.image = self.spacecraft.normal

            if self.release_time <= 0:
                if pygame.key.get_pressed()[pygame.K_SPACE] and self.check:
                    # Create new missile and add it to the space
                    self.anti_spacecraft.missile.create((-1000, -1232))
                    self.space.add(self.anti_spacecraft.missile.shape)

                    self.start_time = pygame.time.get_ticks()
                    self.anti_spacecraft.missile.launched = False
                    self.anti_spacecraft.missile.collided = False
                    self.check = False

                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.end_time = pygame.time.get_ticks()
                    diff = self.end_time - self.start_time

                    self.anti_spacecraft.missile.launch(diff)

                    # Add the missile body to the space
                    self.space.add(self.anti_spacecraft.missile.body)

                    # Reset cool down
                    self.release_time = 120
                    self.check = True

            # Apply gravitational effects to the flying missile
            if self.anti_spacecraft.missile.body:
                self.anti_spacecraft.missile.apply_gravity()

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

        if self.release_time > 0:
            self.release_time -= 1
            self.start_time = pygame.time.get_ticks()
            cooldown = max(self.release_time, 0) * 1.5

            pygame.draw.line(display, pygame.color.THECOLORS["blue"], (1125, 750), (1125, 750 - cooldown), 10)
        else:
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.anti_spacecraft.missile.body:

                self.anti_spacecraft.missile.prepare_for_launch(self.anti_spacecraft.cannon_b,
                                                                self.anti_spacecraft.cannon_s)

                current_time = pygame.time.get_ticks()
                diff = current_time - self.start_time
                power = max(min(diff, 750), 0)
                h = power / 4
                pygame.draw.line(display, pygame.color.THECOLORS["red"], (1150, 750), (1150, 750 - h), 10)

        """
        Missile sprite blit
        """
        if self.anti_spacecraft.missile.shape:
            m, missile_img = self.anti_spacecraft.missile.get_attachment_coordinates(self.anti_spacecraft.missile.body,
                                                                     self.screen_height)
            self.anti_spacecraft.missile.rect = missile_img.get_rect(left=m[0], top=m[1])
            if self.anti_spacecraft.missile.ready_to_blit():
                display.blit(missile_img, self.anti_spacecraft.missile.rect)

        # Landing pad Sprite
        display.blit(self.landing_pad.image, self.landing_pad.rect)

        ###########################
        # Anti-Spacecraft fuel bar
        ##########################
        self.anti_spacecraft.fuel_bar(display, self.screen_height)

        ###########################
        # Spacecraft health bar
        ##########################
        self.spacecraft.health_bar(display, self.screen_height)

        # Attach the spacecraft sprite to the pymunk shape
        p, sc_sprite = self.spacecraft.get_attachment_coordinates(self.spacecraft.body, self.screen_height)
        self.spacecraft.rect = sc_sprite.get_rect(left=p[0], top=p[1])
        display.blit(sc_sprite, self.spacecraft.rect)

        p, rotated_body_img = self.anti_spacecraft.body_sprite.get_attachment_coordinates(
            self.anti_spacecraft.chassis_b, self.screen_height)
        self.anti_spacecraft.body_sprite.rect = rotated_body_img.get_rect(left=p[0], top=p[1] - 15)
        display.blit(rotated_body_img, self.anti_spacecraft.body_sprite.rect)

        # Move the Anti-Spacecraft if buttons pressed
        self.anti_spacecraft.apply_force()

        self.spacecraft.terrain_collision_cooldown += 1
        if self.spacecraft.terrain_collision_cooldown > 120:
            self.spacecraft.terrain_collision = True
            self.spacecraft.terrain_collision_cooldown = 0

        if self.spacecraft.health <= 0:
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

    def add_objects_to_space(self):
        # Anti-spacecraft Parts (represent the whole vehicle)
        self.space.add(self.anti_spacecraft.wheel1_b, self.anti_spacecraft.wheel1_s)
        self.space.add(self.anti_spacecraft.wheel2_b, self.anti_spacecraft.wheel2_s)
        # self.space.add(self.anti_spacecraft.wheel3_b, self.anti_spacecraft.wheel3_s)
        self.space.add(self.anti_spacecraft.chassis_b, self.anti_spacecraft.chassis_s)
        self.space.add(self.anti_spacecraft.cannon_b, self.anti_spacecraft.cannon_s)
        self.space.add(self.anti_spacecraft.pin1, self.anti_spacecraft.pin2, self.anti_spacecraft.pin3,
                       self.anti_spacecraft.pin4, self.anti_spacecraft.pin5, self.anti_spacecraft.pin6)
        # self.anti_spacecraft.pin9, self.anti_spacecraft.pin10)
        self.space.add(self.anti_spacecraft.pin8, self.anti_spacecraft.cannon_mt)

        # Spacecraft object
        self.space.add(self.spacecraft.body, self.spacecraft.shape)

        self.space.add(self.pymunk_landing_pad)

    def start_collision_handlers(self):
        self.missile_and_terrain.begin = self.missile_terrain_collision_begin
        self.missile_and_spacecraft_handler.begin = self.missile_spacecraft_collision_begin
        self.spacecraft_and_terrain_handler.begin = self.spacecraft_terrain_collision_begin

        self.missile_and_spacecraft_handler.pre_solve = self.collision_pre
        self.missile_and_spacecraft_handler.post_solve = self.collision_post_solve
        self.missile_and_spacecraft_handler.separate = self.collision_separate
        self.missile_and_terrain.pre_solve = self.collision_pre
        self.missile_and_terrain.post_solve = self.collision_post_solve
        self.missile_and_terrain.separate = self.collision_separate
        self.spacecraft_and_terrain_handler.pre_solve = self.collision_pre
        self.spacecraft_and_terrain_handler.post_solve = self.collision_post_solve
        self.spacecraft_and_terrain_handler.separate = self.collision_separate

    """
    The following 4 methods(callbacks) - [collision_begin, collision_pre, collision_post, collision_separate] 
       are required for each collision handler to work
    The only one we are using is the one checking for the beginning of the collision
    That is why we have implemented 3 collision handler begin methods. To check between:
      1 - Missile and Terrain
      2 - Spacecraft and Missile
      3 - Spacecraft and Terrain
    Each 'contact handler' (collision_begin method) is implementing its own functionality
    The rest are not doing anything so we can use the same ones for all handlers
    """

    def missile_terrain_collision_begin(self, arbiter, space, data):
        self.space.remove(self.anti_spacecraft.missile.body)
        self.space.remove(self.anti_spacecraft.missile.shape)
        self.anti_spacecraft.missile.collided = True

        return True

    def spacecraft_terrain_collision_begin(self, arbiter, space, data):
        if self.spacecraft.terrain_collision:
            self.spacecraft.receive_damage(20)
        self.spacecraft.terrain_collision = False
        return True

    def missile_spacecraft_collision_begin(self, arbiter, space, data):
        self.spacecraft.receive_damage(20)
        self.player2_pts += 10
        self.anti_spacecraft.missile.collided = True

        self.space.remove(self.anti_spacecraft.missile.body)
        self.space.remove(self.anti_spacecraft.missile.shape)

        return True

    def collision_post_solve(self, arbiter, space, data):
        pass

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
        msg_rect.center = ((self.screen_width / 2), (self.screen_height / 2.3))
        instructions = self.font_warning.render("Game ended. Press ENTER to see results.", False, CYAN)
        instructions_rect = instructions.get_rect()
        instructions_rect.center = ((self.screen_width / 2), (self.screen_height / 2))

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
