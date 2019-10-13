"""
Player class
"""
from PyMunk.constants import *
import pymunk


class Player:

    def __init__(self, mass=DEFAULT_MASS, moment=DEFAULT_MOMENT, position=(G_SCREEN_WIDTH/2, G_SCREEN_HEIGHT/2)):
        self.body = pymunk.Body(mass, moment)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, ANTI_SPACECRAFT_WHEEL_SIZE)
        self.shape.friction = DEFAULT_FRICTION
        self.force = DEFAULT_FORCE

    def apply_force(self):
        self.body.apply_force_at_local_point(self.force, self.body.position)

    def force_right(self):
        self.force = (ANTI_SPACECRAFT_MOVE_FORCE, 0)

    def force_left(self):
        self.force = (-ANTI_SPACECRAFT_MOVE_FORCE, 0)
