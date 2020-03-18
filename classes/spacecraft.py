from constants import *
from .sprite_class import Sprite
from random import randint
import pymunk
from math import degrees


class Spacecraft(Sprite):
    """ Changing the Sprite class to work for our solution - to create static objects(background, obstacles, etc.)"""

    def __init__(self):
        # call Sprite initializer (this creates an image surface object, a Rectangle object and provides
        # the 'get_attachment_coordinates() method).
        super().__init__('frames/lander.gif')

        # This variable holds the rotated image if the lander is being rotated or the original image by default
        self.normal = self.image
        
        # This variable holds the image for the case when thrust is applied and must appear. The original is swapped 
        # with this image every time the activate engine button is pressed on keyboard
        self.activated_img = pg.image.load("frames/lander_active.png")
        
        # This method takes the actual size of the image ignoring its transparent parts
        self.mask = pg.mask.from_surface(self.image)

        """Initializing lander's attributes: 
            the default angle, its lives, the current altitude after spawn, 
            the damage percentage and setting random velocities for the lander moving on x and y"""
        # Health bar
        self.health = 100
        self.damage = 0
        self.crashed = False
        self.terrain_collision_cooldown = 0
        self.terrain_collision = True

        """Initializing the pymunk representation of the space craft. The list of vertices is used by Pymunk to create 
        the shape of the spacecraft body. Each tuple in the list is a coordinate of a point. Linking all points creates
        the shape. Then we initialize the mass, moment, Body and Shape objects. We set the friction that acts on the 
        craft and adjust its color and collision type. Lastly, we position the spacecraft."""
        self.polygon_vertices = [(-30, -25), (-10, -25), (10, -25), (30, -25), (0, 35)]
        self.mass = 0.6
        self.moment = pymunk.moment_for_poly(self.mass, self.polygon_vertices)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly(self.body, self.polygon_vertices)
        self.shape.friction = 0.5
        self.shape.color = BLACK_INVISIBLE
        # Setting the spacecraft collision type so the collision handler can check for it
        self.shape.collision_type = 2
        self.body.position = 600, 700

    # Change health bar color as the health drops
    def health_bar(self, display, height):
        if self.health >= 75:
            health_color = GREEN
        elif self.health >= 50:
            health_color = YELLOW
        elif self.health <= 0:
            health_color = WHITE
        else:
            health_color = RED

        # White bar underneath to make the health drop visible
        pg.draw.line(display, WHITE, flipy((self.body.position - (80, 45)), height),
                     flipy((self.body.position[0] + 75,
                            self.body.position[1] - 45), height), 10)
        # Actual health bar
        pg.draw.line(display, health_color, flipy((self.body.position - (80, 45)), height),
                     flipy((self.body.position[0] + 75 - self.damage,
                            self.body.position[1] - 45), height), 10)

    # Apply thrust force to the spacecraft (make it fly)
    def apply_thrust(self):
        self.body.apply_impulse_at_local_point((self.body.angle, 20), (0, 0))  # Generate and apply an impulse
        self.image = self.activated_img  # Swap the current image with the activated for the blit() method

    def reset_stats(self):
        """ Method resets all the attributes of the lander to default """
        self.rect.left = randint(0, 1200 - self.rect.width)  # spawns the ship on a different place on the top
        self.rect.top = 0
        self.damage = 0

    def receive_damage(self, dmg):
        # Decrease health
        self.health -= dmg
        self.damage += dmg * 1.5  # This variable is used in the health bar, to ensure that it decreases properly

    def get_landing_condition(self):
        """ The method is responsible for checking spacecraft-related landing conditions. It is called every time the
            spacecraft collides with the landing pad sprite. On such a collision the health of the spacecraft must be
            more than 0, its rotation angle must be at max 10 in both directions and its falling velocity must be less
            than 300 pixels per frame."""
        return (self.health > 0 and (-10 <= degrees(self.body.angle) <= 10) and
                (-300 < self.body.velocity.y < 20))
