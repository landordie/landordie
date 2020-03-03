from math import sin, cos, radians
import pygame as pg
from pymunk import Vec2d
from constants import *
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
        # Health bar
        self.health = 100
        self.damage = 0
        self.crashed = False
        self.counter_gravity = False

        self.triangle = [(-55, -30), (55, -30), (0, 50)]
        self.mass = 0.5
        self.moment = pymunk.moment_for_poly(self.mass, self.triangle)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly(self.body, self.triangle)
        self.shape.friction = 0.5
        self.body.position = 600, 700
        self.body.angle = self.rotation_angle

    # Change health bar color as the health drops
    def health_bar(self, display):
        if self.health >= 75:
            health_color = GREEN
        elif self.health >= 50:
            health_color = YELLOW
        else:
            health_color = RED

        health = max(self.health, 0)
        pg.draw.line(display, health_color, flipy((self.body.position - (80, 45))),
                         flipy((self.body.position[0] - 25 + health,
                                self.body.position[1] - 45)), 10)  # Health bar

    # Apply thrust force to the spacecraft (make it fly)
    def apply_thrust(self):
        self.body.apply_impulse_at_local_point((self.body.angle, 30), (0,0))

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
        # Decrease health
        self.health -= dmg
        self.damage += dmg

    def get_landing_condition(self):
        return (self.damage < 100 and (-7 <= self.body.angle <= 7)
                (-5 < self.body.velocity < 5))
