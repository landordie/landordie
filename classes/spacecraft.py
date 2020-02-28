from math import sin, cos, radians
import pygame as pg
from pymunk import Vec2d
import constants
from .sprite_class import Sprite
from random import randint, uniform
import pymunk


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1] + 800)


class Spacecraft(Sprite):
    """ Changing the Sprite class to work for our solution - to create static objects(background, obstacles, etc.)"""

    def __init__(self, max_width):
        super().__init__('frames/lander.png')  # call Sprite initializer
        self.width = max_width
        # This variable holds the rotated image if the lander is being rotated or the original image by default
        self.rotatedImg = self.image
        # This method takes the actual size of the image ignoring its transparent parts
        self.mask = pg.mask.from_surface(self.rotatedImg)

        """Initializing lander's attributes: 
            the default angle, its lives, the current altitude after spawn, 
            the damage percentage and setting random velocities for the lander moving on x and y"""
        self.velocity_x = uniform(-1.0, 1.0)
        self.velocity_y = uniform(0.0, 1.0)
        self.rotation_angle = 0
        self.damage = 0
        self.crashed = False
        self.counter_gravity = False

        self.triangle = [(-55, -30), (55, -30), (0, 50)]
        self.mass = 1
        self.moment = pymunk.moment_for_poly(self.mass, self.triangle)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly(self.body, self.triangle)
        self.shape.friction = 0.5
        self.body.position = 600, 700
        self.body.angle = self.rotation_angle

    def fall_down(self):
        """ Method implements the effect of Mars'es gravitation on the lander """

        if not self.counter_gravity:
            self.velocity_y += 0.03
        else:
            if self.velocity_y > 0:
                self.velocity_y -= 0.03
                if self.velocity_y < 0:
                    self.velocity_y = 0

        self.rect.bottom += self.velocity_y
        self.rect.left += self.velocity_x

        # check and control the behaviour of the lander according its position on the screen size
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity_x = uniform(-1.0, 1.0)

        if self.rect.right > self.width:
            self.rect.right = self.width
            self.velocity_x = uniform(-1.0, 1.0)

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = uniform(0.0, 1.0)

    def rotate(self, direction=None):  # rotates ship to the left or right by 1 degree
        if direction == "left":
            self.rotation_angle += 1 % 360
        elif direction == 'right':
            self.rotation_angle -= 1 % 360
        self.rotatedImg = pg.transform.rotate(self.image, self.rotation_angle)

    def activate_engines(self):
        """ This method is helps the ship to counter-react the gravitation effect of the planet """
        self.velocity_y -= 0.33 * cos(radians(self.rotation_angle))
        self.velocity_x += 0.33 * sin(radians(-self.rotation_angle))

    def gravity_control_system(self):
        self.counter_gravity = not self.counter_gravity

    def get_altitude(self):  # calculates the current altitude of the ship
        return 1000 - (self.rect.top * 1.436)

    def reset_stats(self):
        """ Method resets all the attributes of the lander to default """
        self.rect.left = randint(0, 1200 - self.rect.width)  # spawns the ship on a different place on the top
        self.rect.top = 0
        self.velocity_y = uniform(0.0, 1.0)
        self.velocity_x = uniform(-0.1, 1.0)
        self.rotatedImg = self.image
        self.rotation_angle = 0
        self.damage = 0

    def receive_damage(self, dmg):
        self.damage += dmg

    def get_landing_condition(self):
        return (self.damage < 100 and (-7 <= self.rotation_angle <= 7)
                and (-5 < self.velocity_y < 5) and (-5 < self.velocity_x < 5))
