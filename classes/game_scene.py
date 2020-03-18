import math
import random
import pymunk
from pymunk import pygame_util
from classes.landing_pad import LandingPad
from classes.spacecraft import Spacecraft
from .scene_base import *
from .result_scene import ResultScene
from .anti_spacecraft import AntiSpaceCraft
from .controls import Controls
from pygame.time import Clock as GameClock
from .star_field import StarField


class GameScene(SceneBase):
    # Creates pymunk shape filter object which enables objects to pass through each other, do not collide
    border_sf = pymunk.ShapeFilter(group=2)

    def __init__(self):
        # TODO: !!! EXPLAIN ALL THE TODO's in this file in the report !!!
        """This constructor method initializes the Game Scene class. It is responsible for controlling the gameplay.
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
        SceneBase.__init__(self)  # This statement ensures that this class inherits its behaviour from its Superclass
        # Abstract methods of all scenes (ProcessInput, Render, Update, etc.), screen resolutions, text fonts,
        # general text drawing methods and so on.

        # Initialize the environment and all the objects except the players objects: -----------------------------------
        #        terrain, borders, landing pad, stars, background, etc.
        self.space = pymunk.Space()  # Pymunk Space - the active game environment
        self.space.gravity = EARTH_GRAVITY  # Adjust the environment characteristics
        self.borders()  # This creates the solid borders encapsulating the space
        self.random_terrain()  # Generates the random terrain of the space

        # Initialize the Landing pad object (creates both pymunk body,shape and pygame sprite surface)
        self.landing_pad = LandingPad(self.screen_width - 100, self.screen_height)  # Pygame representation
        # Pymunk representation - A pymunk segment object that is created based on the position of the pygame sprite
        self.pymunk_landing_pad = pymunk.Segment(self.space.static_body, flipy((self.landing_pad.rect.left + 14,
            self.landing_pad.rect.top + 16), self.screen_height), flipy((self.landing_pad.rect.right - 14,
            self.landing_pad.rect.top + 16), self.screen_height), 5)

        # This variable fetches the game controls from the options menu (updated every game)
        self.ctrls = Controls.get_controls()  # Controls is a static class which handles the game controls

        self.star_field = StarField(self.screen_width, self.screen_height)  # The stars moving in the background
        self.background = pg.image.load("frames/splash_BG.jpg")  # A background image
        self.release_time = 0  # Used for making the cooldown function of the shooter. Between 0 and 120 frames (2 sec)
        # --------------------------------------------------------------------------------------------------------------

        # Anti-spacecraft object
        self.anti_spacecraft = AntiSpaceCraft()

        # Spacecraft object
        self.spacecraft = Spacecraft()

        # Collision handlers look for shapes with certain collision types
        # 2 -> spacecraft which is set in the class constructor
        # 3 -> missile which is set in the anti_spacecraft.create_missile() method
        # 4 -> wall segments
        self.missile_and_spacecraft_handler = self.space.add_collision_handler(2, 3)
        self.missile_and_terrain = self.space.add_collision_handler(4, 3)
        self.spacecraft_and_terrain_handler = self.space.add_collision_handler(2, 4)

        # We must set the 4 callback methods of the handlers
        self.start_collision_handlers()

        # Add spacecraft and anti-spacecraft pymunk representations to space
        self.add_objects_to_space()

        # These variables are used for score counting, cooldowns, collision verifications and other checks
        self.player1_pts = 0
        self.player2_pts = 0
        self.end_time = 0
        self.start_time = 0
        self.check = True

    # TODO: !!! THIS IS IMPORTANT, TOO !!!
    """ The next sequence of 5 methods (ProcessInput(), Update(), Render(), SwitchToScene(), Terminate()) are inherited 
        from Scene Base and have their own implementation in each scene. Therefore, the purpose of each of them is 
        explained in the SceneBase class. """

    def ProcessInput(self, events, pressed_keys):

        # -------------------------------------------Start of block-----------------------------------------------------
        # This block responds to the user input for controlling the vehicles. A dictionary (CONTROL_DICT) located in
        # constants.py is used to provide changeability of the default controls. It  maps all the available pygame.KEY
        # objects to Strings (the key names), so when user changes a control in the OptionsScene the game updates
        keys = pygame.key.get_pressed()  # Get the pressed keys (a list that has 0 or 1 next to each keyboard key)

        # Controls of the anti-spacecraft except shooting (it is handled separately further down)
        # Get the key object mapped to the description at index 5 in the # user-defined controls list
        # All the if else checks in this block work in the same fashion
        if keys[CONTROL_DICT[self.ctrls[5]]]:
            self.anti_spacecraft.force_right()  # If
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

        # Controls of spacecraft (it is controllable only if it hasn't crashed)
        if not self.spacecraft.crashed:
            # Rotate spacecraft (in radians)
            if keys[CONTROL_DICT[self.ctrls[0]]]:
                self.spacecraft.body.angle += math.radians(2)
            if keys[CONTROL_DICT[self.ctrls[2]]]:
                self.spacecraft.body.angle -= math.radians(2)
            if keys[CONTROL_DICT[self.ctrls[1]]]:
                self.spacecraft.apply_thrust()
        # ---------------------------------------------End of block ----------------------------------------------------

        # The following for-loop checks each event that has been passed to the ProcessInput method
        for event in events:
            # TODO: Remove 'if' in final code
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

            # This stop displaying the thrust once the key responsible for activating spacecraft engines is released
            if event.type == pygame.KEYUP and event.key == CONTROL_DICT[self.ctrls[1]]:
                self.spacecraft.image = self.spacecraft.normal

            # -----------------------------------------Start of block---------------------------------------------------
            # The following block is responsible for shooting missiles from the anti-spacecraft vehicle
            # If the cooldown is 0 (Player 1 hasn't shot in the last 2 seconds)
                # Check if the shooting button is pressed and initialize the mechanism
            if self.release_time <= 0:
                if pygame.key.get_pressed()[CONTROL_DICT[self.ctrls[7]]] and self.check:
                    # Create new Pymunk missile and add its shape to the space, body will be added later
                    # It has to be created away from the space so that it doesn't collide with anything.
                    # It will be positioned in the Render method
                    self.anti_spacecraft.missile.create((-1000, -1232))
                    self.space.add(self.anti_spacecraft.missile.shape)

                    # This variable records when the shooting button is pressed
                    # (it will be used to calculate the strength of the impulse that shoots the bullet)
                    self.start_time = pygame.time.get_ticks()
                    self.anti_spacecraft.missile.launched = False
                    self.anti_spacecraft.missile.collided = False
                    self.check = False

                # If the shooting key is released calculate the impulse and add the
                # pymunk body of the missile to the space
                if event.type == pygame.KEYUP and event.key == CONTROL_DICT[self.ctrls[7]]:
                    self.end_time = pygame.time.get_ticks()
                    diff = self.end_time - self.start_time

                    self.anti_spacecraft.missile.launch(diff)

                    # Add the missile body to the space
                    self.space.add(self.anti_spacecraft.missile.body)

                    # Reset cool down
                    self.release_time = 120
                    self.check = True
            # ------------------------------------------End of block ---------------------------------------------------

            # Apply gravitational effects to the flying missile
            if self.anti_spacecraft.missile.body:
                self.anti_spacecraft.missile.apply_gravity()

    def Update(self):
        pass

    def Render(self, screen):
        # A screen (Pygame surface object or the environment) is passed to the method from its predecessor scene)
        display = screen.get_surface()  # Convert the screen into display
        screen.set_mode((self.screen_width, self.screen_height))  # Set the resolution of the screen
        display.blit(self.background, (0, 0))  # Position the background on the display (0, 0) is the position from
        # which the image has to start. It is positioned based on top-left corner of the image and 0,0 is top-left
        # corner of Pygame coordinate system
        self.star_field.draw_stars(display)  # Complement the background with some falling star effects

        # -------------------------------------------Start of block-----------------------------------------------------
        # These three statements are responsible for updating the pymunk space on each frame
        # They also stabilise the connection b/w pygame and pymunk objects on the screen
        self.space.step(1. / FPS)
        draw_options = pymunk.pygame_util.DrawOptions(display)
        self.space.debug_draw(draw_options)

        # This block renders the missiles on the screen. While there is a cooldown active (the if statement),
        # a blue line is drawn on the screen which shows the remaining cooldown time
        if self.release_time > 0:
            self.release_time -= 1
            self.start_time = pygame.time.get_ticks()
            cooldown = max(self.release_time, 0) * 1.5

            pygame.draw.line(display, pygame.color.THECOLORS["blue"], (1125, 750), (1125, 750 - cooldown), 10)
        # When the cooldown is not active and a shooting key is pressed, the missile is being positioned relative to
        # the position of the cannon and a red line is drawn on the screen that indicates the strength of the impulse
        else:
            if pygame.key.get_pressed()[CONTROL_DICT[self.ctrls[7]]] and self.anti_spacecraft.missile.body:
                # Position the missile relative to the current cannon position
                # Adjust the Pymunk missile's rotation angle to be exactly the same the cannon's
                self.anti_spacecraft.missile.prepare_for_launch(self.anti_spacecraft.cannon_b,
                                                                self.anti_spacecraft.cannon_s)

                # Display the red line on the screen, which increases with the time the shooting key is pressed
                current_time = pygame.time.get_ticks()
                diff = current_time - self.start_time
                power = max(min(diff, 750), 0)
                h = power / 4
                pygame.draw.line(display, pygame.color.THECOLORS["red"], (1150, 750), (1150, 750 - h), 10)

        # This piece of code is displaying the pygame sprite (the image) for the missile
        if self.anti_spacecraft.missile.shape:
            # TODO: Make sure to explain this in report
            # The method get_attachment_coordinates() determines the exact position the pygame object must be placed at
            # It converts pymunk coordinates into pygame ones and also ensures that the image of the missile is rotated
            # in the same angle as its pymunk body. The angles in pymunk are in radians in pygame in degrees.
            m, missile_img = self.anti_spacecraft.missile.get_attachment_coordinates(self.anti_spacecraft.missile.body,
                                                                     self.screen_height)
            self.anti_spacecraft.missile.rect = missile_img.get_rect(left=m[0], top=m[1])
            # If there isn't a collision display the image on screen and the missile is launched
            if self.anti_spacecraft.missile.ready_to_blit():
                display.blit(missile_img, self.anti_spacecraft.missile.rect)
        # --------------------------------------------End of block -----------------------------------------------------

        # Show the Landing pad Sprite on screen
        display.blit(self.landing_pad.image, self.landing_pad.rect)

        ###########################
        # Anti-Spacecraft fuel bar
        ###########################
        # Display the Anti-Spacecraft fuel bar - the part that has been consumed turns red; initially it is green.
        self.anti_spacecraft.fuel_bar(display, self.screen_height)

        ###########################
        # Spacecraft health bar
        ###########################
        # Spacecraft health bar - it is green, and as the health of the craft drops its colour changes to yellow and red
        self.spacecraft.health_bar(display, self.screen_height)

        # Attach the spacecraft sprite to the pymunk shape
        p, sc_sprite = self.spacecraft.get_attachment_coordinates(self.spacecraft.body, self.screen_height)
        self.spacecraft.rect = sc_sprite.get_rect(left=p[0], top=p[1])
        display.blit(sc_sprite, self.spacecraft.rect)

        # Attach the sprite of the anti-spacecraft to its pymunk body object
        p, rotated_body_img = self.anti_spacecraft.body_sprite.get_attachment_coordinates(
            self.anti_spacecraft.chassis_b, self.screen_height)
        self.anti_spacecraft.body_sprite.rect = rotated_body_img.get_rect(left=p[0], top=p[1] - 15)
        display.blit(rotated_body_img, self.anti_spacecraft.body_sprite.rect)

        # Move the Anti-Spacecraft if buttons pressed
        self.anti_spacecraft.apply_force()

        # Introduce a cooldown function for the collision between the terrain and the spacecraft
        # Before a collision occurs this doesn't do anything
        # After a collision with the terrain, a new one can occur after minimum 2 seconds (120 Frames)
        # This ensures that the spacecraft doesn't take additional damage while standing on the ground for some time
        self.spacecraft.terrain_collision_cooldown += 1
        if self.spacecraft.terrain_collision_cooldown > 120:
            self.spacecraft.terrain_collision = True
            self.spacecraft.terrain_collision_cooldown = 0

        # If the spacecraft has no health left, pause the game and display a notification
        if self.spacecraft.health <= 0:
            paused = self.pause_game('no HP', display)
            if paused:
                self.Terminate()
            else:
                self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))

        # If a landing attempt is performed and the conditions passes (e.g velocity is not too high, the position is
        # correct, the angle of rotation is not too big, etc.) increment the score of the craft player and stop game
        if pygame.sprite.collide_mask(self.landing_pad, self.spacecraft):
            if self.landing_pad.check_for_landing_attempt(self.spacecraft):
                paused = self.pause_game('landed', display)
                if paused:
                    self.Terminate()
                else:
                    self.player1_pts += 50
                    self.SwitchToScene(ResultScene(self.player1_pts, self.player2_pts))
# ======================================================================================================================

    """ All these methods below are helpers which are used for simplifying the above code."""
    def add_objects_to_space(self):  # This adds all the components of the anti-spacecraft (cannon, wheels, chassis,
        # pin-joints), the spacecraft body and shape and the landing pad body to the Pymunk space

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

        # Landing pad object
        self.space.add(self.pymunk_landing_pad)

    def start_collision_handlers(self):
        # This method initializes all the collision handlers between different Pymunk objects
        # An explanation is given below this method
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

    # When a missile collides with the terrain it disappears except in the cases where the missile is still in the
    # cannon of the anti-spacecraft (not active missile)
    def missile_terrain_collision_begin(self, arbiter, space, data):
        if not pygame.key.get_pressed()[CONTROL_DICT[self.ctrls[7]]] and self.release_time > 0:
            self.space.remove(self.anti_spacecraft.missile.body)
            self.space.remove(self.anti_spacecraft.missile.shape)
            self.anti_spacecraft.missile.collided = True

        return True

    # When a collision b/w terrain and spacecraft occurs and there is no cooldown for the collision detector,
    # spacecraft takes 20 damage
    def spacecraft_terrain_collision_begin(self, arbiter, space, data):
        if self.spacecraft.terrain_collision:
            self.spacecraft.receive_damage(20)
        self.spacecraft.terrain_collision = False  # The control variable is reset
        return True

    # When a missile collides with the spacecraft it disappears, deals damage to the craft and increments player 1's
    # score, except in the cases where the missile is still in the cannon of the anti-spacecraft (not active missile)
    def missile_spacecraft_collision_begin(self, arbiter, space, data):
        if not pygame.key.get_pressed()[CONTROL_DICT[self.ctrls[7]]]:
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
        """ The method pauses the game after the player crashes, lands correctly or has no HP left and displays a
        message, till the Return key is pressed """
        msg = ''

        if msg_type == 'landed':
            msg = self.font_warning.render("Successful Landing!", False, (13, 109, 24))
        elif msg_type == 'crashed':
            msg = self.font_warning.render("The spacecraft has crashed!", False, (255, 0, 6))
        elif msg_type == 'no HP':
            msg = self.font_warning.render("The spacecraft has been destroyed (0 HP left)", False, (255, 0, 6))

        # TODO: !!!EXPLAIN THE SCREEN HEIGHT AND WIDTH GLOBALITY (they are general for all and controlled by one)
        # Here the message position is adjusted, relative to the screen height and width
        msg_rect = msg.get_rect()
        msg_rect.center = ((self.screen_width / 2), (self.screen_height / 2.3))
        instructions = self.font_warning.render("Game ended. Press ENTER to see results.", False, CYAN)
        instructions_rect = instructions.get_rect()
        instructions_rect.center = ((self.screen_width / 2), (self.screen_height / 2))

        # Display the message
        screen.blit(msg, msg_rect)
        screen.blit(instructions, instructions_rect)

        while True:
            # Enter an infinite loop which can be interrupted by quitting or pressing Return key on keyboard
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
        Create a random terrain from a sequence of linked pymunk segment objects.
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
        self.space.add(terrain)

    def borders(self):
        # This method creates the borders of the screen.
        border_left = pymunk.Segment(self.space.static_body, (0, 0), (0, self.screen_height), 10)
        border_right = pymunk.Segment(self.space.static_body, (self.screen_width, 0), (self.screen_width,
                                                                                       self.screen_height), 10)
        border_top = pymunk.Segment(self.space.static_body, (0, self.screen_height), (self.screen_width,
                                                                                      self.screen_height), 10)
        border_bottom = pymunk.Segment(self.space.static_body, (0, 0), (self.screen_width, 0), 75)
        border_bottom.friction = TERRAIN_FRICTION
        border_bottom.color = DARK_GREY

        # Add all borders to the same group, to enable overlapping in the corners
        border_top.filter = GameScene.border_sf
        border_bottom.filter = GameScene.border_sf
        border_right.filter = GameScene.border_sf
        border_left.filter = GameScene.border_sf

        # Set the collision types so that the collision handlers check for them
        border_top.collision_type = 4
        border_left.collision_type = 4
        border_right.collision_type = 4
        border_bottom.collision_type = 4

        # Add all to the space
        self.space.add(border_left, border_right, border_top, border_bottom)


"""End of file"""
