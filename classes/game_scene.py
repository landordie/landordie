"""
'game_scene.py' module.
Used in instantiation of the Game scene (window).
"""
from math import pi, radians
import random
import pymunk as pm
from pymunk import pygame_util
from pygame.time import Clock as GameClock
from .landing_pad import LandingPad
from .spacecraft import Spacecraft
from .scene_base import SceneBase
from .result_scene import ResultScene
from .anti_spacecraft import AntiSpaceCraft
from .controls import Controls
from .star_field import StarField
from constants import *

# TODO: NO GAMEPLAY INSTRUCTIONS WHATSOEVER... TRIAL AND ERROR - FUNDAMENTAL METHOD OF PROBLEM SOLVING
#  ( INCLUDE IN REP!)


class GameScene(SceneBase):
    """GameScene subclass implementation."""
    border_sf = pm.ShapeFilter(group=2)  # Game borders filter which allows shape grouping for collision avoidance

    def __init__(self):
        # TODO: !!! EXPLAIN ALL THE TODO's in this file in the report !!!
        """
        Virtually private constructor which initializes the Game scene. It is responsible for
        controlling the game features. Here all the game objects are initialized and used in
        one combined environment. That way we can use the physics engine behind Pymunk (chipmunk)
        together with the images, surfaces and user-input handlers provided by Pygame.
        """
        super().__init__()  # Call the super class (SceneBase) initialization method. This
        # statement ensures that this class inherits its behaviour from its Superclass.
        # Abstract methods of all scenes (process_input(), update(), render(), etc.), screen
        # resolutions, text fonts, general text drawing methods and so on.
        # --------------------------------------------------------------------------------------------------------------
        # Pygame environment where all the sprites(images) are managed. This environment also displays
        # the text and is responsible for opening and closing new windows, checking button clicks and
        # event occurrences.

        # Initialize the environment and all the objects except the players objects:
        # terrain, borders, landing pad, stars, background, etc.
        self.space = pm.Space()  # Pymunk space - the active game environment
        self.space.gravity = EARTH_GRAVITY  # Adjust the environment characteristics
        self.borders()  # Create the solid borders encapsulating the space
        self.random_terrain()  # Generate the random terrain of the space

        # Initialize the Landing pad object (creates both Pymunk body,shape and Pygame sprite surface)
        self.landing_pad = LandingPad(self.screen_width, self.screen_height)  # Pygame representation

        # Pymunk representation - A Pymunk segment object that is created based on the position of
        # the Pygame sprite
        self.pm_landing_pad = self.landing_pad.pymunk_pad(self.space, self.screen_height)
        self.game_controls = Controls.get_controls()  # Fetch the game controls
        self.star_field = StarField(self.screen_width, self.screen_height)  # The stars moving in the background
        self.background = pg.image.load("Assets/frames/splash_BG.jpg")  # A background image
        self.release_time = 0  # Used for making the cooldown function of the shooter.
        # Between 0 and 120 frames (2 sec)
        # --------------------------------------------------------------------------------------------------------------
        # Pymunk space object which represents our physical, realistic world. It creates and
        # handles all the bodies and shapes behind the Pygame sprites. All the physical forces in the
        # Pymunk space act on the bodies of the objects and they then determine what the behaviour of
        # the sprites will be.

        self.anti_spacecraft = AntiSpaceCraft()  # Anti-spacecraft vehicle instance
        self.spacecraft = Spacecraft()  # Spacecraft instance

        # Collision handlers look for shapes with certain collision types
        # 2 -> spacecraft which is set in the class constructor
        # 3 -> missile which is set in the anti_spacecraft.create_missile() method
        # 4 -> wall segments
        self.missile_and_spacecraft_handler = self.space.add_collision_handler(2, 3)
        self.missile_and_terrain = self.space.add_collision_handler(4, 3)
        self.spacecraft_and_terrain_handler = self.space.add_collision_handler(2, 4)

        self.start_collision_handlers()  # Set the 4 callback methods of the handlers
        self.add_objects_to_space()  # Add spacecraft and anti-spacecraft Pymunk representations to space

        self.spacecraft_pts = 0  # Spacecraft player points attribute
        self.anti_spacecraft_pts = 0  # Anti-spacecraft player points attribute

        # Clock attributes to calculate the impulse strength to be applied to the missile
        self.end_time = 0
        self.start_time = 0
        self.clock_img = pg.image.load("Assets/frames/timer.png")  # Load the clock icon image

    # TODO: !!! THIS IS IMPORTANT, TOO !!!
    # The next sequence of 5 methods (process_input(), update(), render(), switch_to_scene(),
    # terminate()) are inherited from the superclass (SceneBase) and have their own implementation in each scene.
    # Therefore, the purpose of each of them is explained in the superclass.

    def process_input(self, events, pressed_keys):
        # -------------------------------------------Start of block-----------------------------------------------------
        # This block responds to the user input for controlling the vehicles. A dictionary (CONTROL_DICT) located in
        # constants.py is used to provide changeability of the default controls. It  maps all the available Pygame.KEY
        # objects to Strings (the key names), so when user changes a control in the OptionsScene the game updates
        keys = pg.key.get_pressed()  # Get the pressed keys (a list that has 0 or 1 next to each keyboard key)

        # Controls of the anti-spacecraft except shooting (it is handled separately further down)
        # Get the key object mapped to the description at index 5 in the # user-defined controls list
        # All the if else checks in this block work in the same fashion

        if self.anti_spacecraft.fuel:  # If the anti-spacecraft still has some fuel left
            # Apply force on the wheels accordingly
            if keys[self.game_controls[5]]:
                self.anti_spacecraft.force_right()  # If
            elif keys[self.game_controls[3]]:
                self.anti_spacecraft.force_left()
            else:
                self.anti_spacecraft.force = DEFAULT_FORCE
        else:  # If out of fuel then stop the wheels
            self.anti_spacecraft.force = DEFAULT_FORCE

        # Anti-spacecraft cannon rotation (in radians)
        if keys[self.game_controls[6]]:
            self.anti_spacecraft.cannon_left()
        elif keys[self.game_controls[4]]:
            self.anti_spacecraft.cannon_right()
        else:
            self.anti_spacecraft.cannon_stop()

        # Controls of spacecraft (it is controllable only if it hasn't crashed)
        if not self.spacecraft.crashed():
            # Rotate spacecraft (in radians)
            if keys[self.game_controls[0]]:
                self.spacecraft.rotate_left()
            if keys[self.game_controls[2]]:
                self.spacecraft.rotate_right()
            if keys[self.game_controls[1]]:
                self.spacecraft.apply_thrust()

        # ---------------------------------------------End of block ----------------------------------------------------

        # Check each event that has been passed to the process_input() method
        for event in events:
            # This stop displaying the thrust once the key responsible for activating spacecraft engines is released
            if event.type == pg.KEYUP and event.key == self.game_controls[1]:
                self.spacecraft.image = self.spacecraft.normal

            # -----------------------------------------Start of block---------------------------------------------------
            # The following block is responsible for shooting missiles from the anti-spacecraft vehicle
            # If the cooldown is 0 ( hasn't shot in the last 2 seconds)
            # Check if the shooting button is pressed and initialize the mechanism
            if self.release_time <= 0:
                if keys[self.game_controls[7]] and self.anti_spacecraft.missile.collided:
                    # Create new Pymunk missile and add its shape to the space, body will be added later
                    # It has to be created away from the space so that it doesn't collide with anything.
                    # It will be positioned in the Render method
                    self.anti_spacecraft.missile.create((-self.screen_width, -self.screen_height))
                    self.space.add(self.anti_spacecraft.missile.shape)

                    # This variable records when the 'shoot' button is pressed
                    # (it will be used to calculate the strength of the impulse that shoots the bullet)
                    self.start_time = pg.time.get_ticks()
                    self.anti_spacecraft.missile.launched = False
                    self.anti_spacecraft.missile.collided = False

                # On releasing the 'shoot' key calculate the time difference, launch the missile
                # and add the Pymunk body of the missile to the space (only when the previously
                # launched missile is already removed from the space)
                elif event.type == pg.KEYUP and event.key == self.game_controls[7] \
                        and self.anti_spacecraft.missile.body not in self.space.bodies:

                    self.end_time = pg.time.get_ticks()  # Get the current time
                    diff = self.end_time - self.start_time  # Calculate time difference
                    self.anti_spacecraft.missile.launch(diff)  # Call launch method
                    self.space.add(self.anti_spacecraft.missile.body)  # Add the missile body to the space
                    self.release_time = 120  # Reset cooldown time
            # ------------------------------------------End of block ---------------------------------------------------

            # Apply gravitational effects to the flying missile
        if self.anti_spacecraft.missile.launched:
            self.anti_spacecraft.missile.apply_gravity()

    def render(self, screen):
        # A screen (Pygame surface object or the environment) is passed to the method from its
        # predecessor scene)
        display = self.adjust_screen(screen)  # Surface

        # Position the background on the display (0, 0) is the position from which the image has
        # to start. It is positioned based on top-left corner of the image and 0,0 is top-left
        # corner of Pygame coordinate system
        display.blit(self.background, (0, 0))
        self.star_field.draw_stars(display)  # Complement the background with some falling star effects

        # -------------------------------------------Start of block-----------------------------------------------------
        # These three statements are responsible for updating the Pymunk space on each frame
        # They also stabilise the connection b/w Pygame and Pymunk objects on the screen
        self.space.step(1. / FPS)
        draw_options = pm.pygame_util.DrawOptions(display)
        self.space.debug_draw(draw_options)

        # This block renders the missiles on the screen. While there is a cooldown active
        # (the if statement), a blue line is drawn on the screen which shows the remaining cooldown time
        if self.release_time > 0:
            self.release_time -= 1
            self.start_time = pg.time.get_ticks()
            cooldown = max(self.release_time, 0) * 1.5
            loc = (self.screen_width * .9, self.screen_height * .95)  # Location coordinates
            display.blit(self.clock_img, (loc[0] - self.clock_img.get_size()[0] // 2,  # Display a clock icon
                                          loc[1] - 190 - self.clock_img.get_size()[1]))
            pg.draw.rect(display, LIGHT_BLUE, (loc[0] - 5, loc[1] - 187.5, 12, 190), 3)  # Draw a border for the bar
            pg.draw.line(display, BLUE, loc, (loc[0], loc[1] - cooldown), 10)  # Draw the cooldown bar

        # When the cannon is on cooldown and the 'shoot' key is pressed, the missile is being
        # positioned relative to the position of the cannon and a yellow line is drawn on the screen
        # that indicates the strength of the impulse
        elif pg.key.get_pressed()[self.game_controls[7]] and self.anti_spacecraft.missile.body:
            # Position the missile relative to the current cannon position
            # Adjust the Pymunk missile's rotation angle to be exactly the same the cannon's
            self.anti_spacecraft.missile.prepare_for_launch(self.anti_spacecraft.cannon_b,
                                                            self.anti_spacecraft.cannon_s)

            # Display power bar (yellow)
            loc = tuple(x * .95 for x in (self.screen_width, self.screen_height))  # location coordinates
            self.anti_spacecraft.power_bar(self.start_time, loc, 10, display)

        xy = tuple(x * .95 for x in (self.screen_width, self.screen_height))
        self.anti_spacecraft.draw_power_bar_outline(display, xy)

        # This piece of code is displaying the Pygame sprite (the image) for the missile
        if self.anti_spacecraft.missile.shape:
            m, missile_img = self.anti_spacecraft.missile. \
                get_attachment_coordinates(self.anti_spacecraft.missile.body, self.screen_height)
            self.anti_spacecraft.missile.rect = missile_img.get_rect(left=m[0], top=m[1])

            # If there isn't a collision display the image on screen and the missile is launched
            if self.anti_spacecraft.missile.ready_to_blit():
                display.blit(missile_img, self.anti_spacecraft.missile.rect)

        # ----------------------------------------------End of block----------------------------------------------------

        # Attach the sprite of the anti-spacecraft to its Pymunk body object
        p, rotated_body_img = self.anti_spacecraft.body_sprite. \
            get_attachment_coordinates(self.anti_spacecraft.chassis_b, self.screen_height)
        self.anti_spacecraft.body_sprite.rect = rotated_body_img.get_rect(left=p[0], top=p[1] - 15)
        display.blit(rotated_body_img, self.anti_spacecraft.body_sprite.rect)

        self.anti_spacecraft.apply_force()  # Move the anti-spacecraft if buttons pressed

        # Display the anti-spacecraft fuel bar - the part that has been consumed turns red;
        # initially it is green.
        self.anti_spacecraft.fuel_bar(display, self.screen_height)

        display.blit(self.landing_pad.image, self.landing_pad.rect)  # Show the Landing pad Sprite on screen

        # Spacecraft health bar - it is green, and as the health of the craft drops its
        # colour changes to yellow and red
        self.spacecraft.health_bar(display, self.screen_height)
        pos = (self.screen_width * .07, self.screen_height * .04)  # location coordinates
        self.spacecraft.show_stats(display, pos)  # Display the spacecraft stats (velocity and angle)

        # Attach the spacecraft sprite to the Pymunk shape
        p, sc_sprite = self.spacecraft.get_attachment_coordinates(self.spacecraft.body, self.screen_height)
        self.spacecraft.rect = sc_sprite.get_rect(left=p[0], top=p[1])
        display.blit(sc_sprite, self.spacecraft.rect)

        # Introduce a cooldown function for the collision between the terrain and the spacecraft
        # Before a collision occurs this doesn't do anything. After a collision with the terrain,
        # a new one can occur after minimum 2 seconds (120 Frames) This ensures that the spacecraft
        # doesn't take additional damage while standing on the ground for some time
        self.spacecraft.terrain_collision_cd += 1
        if self.spacecraft.terrain_collision_cd > 120:
            self.spacecraft.terrain_collision = True
            self.spacecraft.terrain_collision_cd = 0

        # If a landing attempt is performed and the conditions passes (e.g velocity is not too high,
        # the position is correct, the angle of rotation is not too big, etc.) increment the score
        # of the craft player and stop game
        if self.spacecraft.get_landing_condition():
            c = GREEN
        else:
            c = RED
        self.landing_pad.show_landing_conditions(display, FONT_WARNING, c)

        if pg.sprite.collide_mask(self.landing_pad, self.spacecraft):
            if self.landing_pad.check_for_landing_attempt(self.spacecraft):
                paused = self.pause_game('landed', display)
                if paused:
                    self.terminate()
                else:
                    self.spacecraft_pts += 50
                    self.switch_to_scene(ResultScene(self.spacecraft_pts, self.anti_spacecraft_pts))

        # If the spacecraft has no health left, pause the game and display a notification
        if self.spacecraft.crashed():
            paused = self.pause_game('no HP', display)
            if paused:
                self.terminate()
            else:
                self.switch_to_scene(ResultScene(self.spacecraft_pts, self.anti_spacecraft_pts))

    # ==================================================================================================================
    # Helper methods below

    def add_objects_to_space(self):
        """
        This adds all the components of the anti-spacecraft (cannon, wheels, chassis, pin joints),
        the spacecraft body and shape and the landing pad body to the Pymunk space
        """
        self.anti_spacecraft.add_to_space(self.space)  # Anti-spacecraft Parts (represent the whole vehicle)
        self.space.add(self.spacecraft.body, self.spacecraft.shape)  # Spacecraft body and shape
        self.space.add(self.pm_landing_pad)  # Landing pad

    def start_collision_handlers(self):
        """Initialize all the collision handlers between different Pymunk objects."""
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

    # The following 4 methods(callbacks) - [collision_begin, collision_pre, collision_post,
    # collision_separate] are required for each collision handler to work. The only one we are
    # using is the one checking for the beginning of the collision

    def missile_terrain_collision_begin(self, arbiter, space, data):
        """
        Missile and terrain collision callback method
        :param arbiter: missile and terrain shapes pair and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        :return: True when the missile and the terrain begin contact
        """
        if self.anti_spacecraft.missile.launched:  # If missile is launched
            self.anti_spacecraft.missile.remove_from_space(self.space)  # Remove missile body and shape
        return True

    def spacecraft_terrain_collision_begin(self, arbiter, space, data):
        """
        Spacecraft and terrain collision callback method
        :param arbiter: spacecraft and terrain shapes pair and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        :return: True when the spacecraft and the terrain begin contact
        """
        if self.spacecraft.terrain_collision:
            self.spacecraft.receive_damage(20)  # Inflict damage to the spacecraft
        self.spacecraft.terrain_collision = False  # The control variable is reset
        return True

    # When a missile collides with the spacecraft it disappears, deals damage to the craft and increments player 1's
    # score, except in the cases where the missile is still in the cannon of the anti-spacecraft (not active missile)
    def missile_spacecraft_collision_begin(self, arbiter, space, data):
        """
        Missile and spacecraft collision callback method
        :param arbiter: a pair of missile and spacecraft shapes and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        :return: True when the missile and the spacecraft begin contact
        """
        if self.anti_spacecraft.missile.launched:
            self.spacecraft.receive_damage(20)
            self.anti_spacecraft_pts += 10
            self.anti_spacecraft.missile.remove_from_space(self.space)

        return True

    def collision_post_solve(self, arbiter, space, data):
        """
        Shape collision callback method
        :param arbiter: a pair of shapes and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        """
        pass

    def collision_pre(self, arbiter, space, data):
        """
        Shape collision callback method
        :param arbiter: a pair of shapes and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        :return: True when two shapes are in contact
        """
        if self.pm_landing_pad in arbiter.shapes and self.spacecraft.shape in arbiter.shapes:  # On spacecraft-landing pad collision
            # Generate an impulse that makes it bounce in the air
            self.spacecraft.body.apply_impulse_at_world_point((0, 250), self.spacecraft.body.position)
        return True

    def collision_separate(self, arbiter, space, data):
        """
        Shape collision callback method (just before separating)
        :param arbiter: a pair of shapes and all of the data about their collision
        :param space: unit of simulation
        :param data: data to be manipulated
        """
        pass

    def pause_game(self, msg_type, screen):
        """
        Pause the game after a player crash, correct landing or the spacecraft is out of HP.
        Display a message, till the 'Return' key is pressed
        :param msg_type: specifies the type of message to be displayd
        :param screen: current scene screen window
        :return: True on 'X' button click, False on pressing 'Return' key
        """
        msg = ''

        if msg_type == 'landed':
            msg = FONT_WARNING.render("Successful Landing!", False, (13, 109, 24))
        elif msg_type == 'crashed':
            msg = FONT_WARNING.render("The spacecraft has crashed!", False, (255, 0, 6))
        elif msg_type == 'no HP':
            msg = FONT_WARNING.render("The spacecraft has been destroyed (0 HP left)", False, (255, 0, 6))

        # TODO: !!!EXPLAIN THE SCREEN HEIGHT AND WIDTH GLOBALITY (they are general for all and controlled by one)
        # Here the message position is adjusted, relative to the screen height and width
        msg_rect = msg.get_rect()
        msg_rect.center = ((self.screen_width / 2), (self.screen_height / 2.3))
        instructions = FONT_WARNING.render("Game ended. Press ENTER to see results.", False, CYAN)
        instructions_rect = instructions.get_rect()
        instructions_rect.center = ((self.screen_width / 2), (self.screen_height / 2))

        # Display the message
        screen.blit(msg, msg_rect)
        screen.blit(instructions, instructions_rect)

        while True:
            # Enter an infinite loop which can be interrupted by quitting or pressing Return key on keyboard
            for event in pg.event.get():
                if event.type == pg.QUIT:  # Quit program on 'X' button click
                    return True
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    # Checks if any key is pressed - Resumes the game
                    return False

            pg.display.update()
            GameClock().tick(FPS)

    def random_terrain(self):
        """Create a random terrain from a sequence of linked Pymunk segment objects."""
        terrain_segments = []  # To hold the list of segments that will be added to the space as a terrain

        # Generate the point tuples
        points = [(i, random.randint(self.screen_height // 20, self.screen_height // 7))
                  for i in range(0, self.screen_width + SEGMENT_LENGTH, SEGMENT_LENGTH)]

        # Loop through the point tuples and populate the 'terrain' list
        for i in range(1, len(points)):
            floor = pm.Segment(self.space.static_body, (points[i - 1][0], points[i - 1][1]),
                               (points[i][0], points[i][1]), TERRAIN_THICKNESS)
            floor.friction = TERRAIN_FRICTION
            floor.filter = pm.ShapeFilter(group=0)
            floor.collision_type = 4
            floor.filter = GameScene.border_sf
            terrain_segments.append(floor)
        self.space.add(terrain_segments)

    def borders(self):
        """Create and place the Game scene borders (Pymunk segments)."""
        border_left = pm.Segment(self.space.static_body, (-5, 0), (-5, self.screen_height), 10)
        border_right = pm.Segment(self.space.static_body, (self.screen_width + 5, 0),
                                  (self.screen_width + 5, self.screen_height), 10)
        border_top = pm.Segment(self.space.static_body, (0, self.screen_height + 5),
                                (self.screen_width, self.screen_height + 5), 10)
        border_bottom = pm.Segment(self.space.static_body, (0, 0), (self.screen_width, 0),
                                   self.screen_height * 0.1)
        border_bottom.friction = TERRAIN_FRICTION  # Set the bottom border friction
        border_bottom.color = DARK_GREY  # Set the bottom border color

        # Set the collision types so that the collision handlers check for them
        border_top.collision_type = 4
        border_left.collision_type = 4
        border_right.collision_type = 4
        border_bottom.collision_type = 4
        self.space.add(border_left, border_right, border_top, border_bottom)  # Add the borders to the Pymunk space
