"""
Missile class
"""
import math

import pymunk as pm
from pymunk import Vec2d

from constants import MISSILE_DRAG_CONSTANT
from .sprite_class import Sprite


class Missile(Sprite):

    def __init__(self):
        super().__init__('frames/missile.gif')  # call Sprite initializer
        self.body, self.shape = None, None
        self.launched = False
        self.collided = False

    def create(self, position):
        """
        Create new missile body and shape at specified location
        """
        vs = [(-30, 0), (0, 3), (10, 0), (0, -3)]
        mass = 0.5
        moment = pm.moment_for_poly(mass, vs)
        self.body = pm.Body(mass, moment)
        self.body.position = position

        self.shape = pm.Poly(self.body, vs)
        self.shape.color = (115.0, 148.0, 107.0, 100.0)
        self.shape.friction = .5
        self.shape.collision_type = 3
        self.shape.filter = pm.ShapeFilter(group=1)
        # Setting the missile collision type so the handler can look for it and handle it
        # self.shape.collision_type = 3

    def prepare_for_launch(self, cannon_body, cannon_shape):
        """
        Position the missile for launch (at anti-spacecraft cannon location)
        :param cannon_body: anti-spacecraft cannon body
        :param cannon_shape: anti-spacecraft cannon shape
        """
        self.body.position = cannon_body.position + Vec2d(cannon_shape.radius - 30, 0).rotated(cannon_body.angle)
        self.body.angle = cannon_body.angle + math.pi

    def apply_gravity(self):
        """
        Apply gravitational effects to the launched missile
        """
        pointing_direction = Vec2d(1, 0).rotated(self.body.angle)
        flight_direction = Vec2d(self.body.velocity)
        flight_speed = flight_direction.normalize_return_length()
        dot = flight_direction.dot(pointing_direction)

        drag_force_magnitude = (1 - abs(
            dot)) * flight_speed ** 2 * MISSILE_DRAG_CONSTANT * self.body.mass
        self.body.apply_impulse_at_world_point(drag_force_magnitude * -flight_direction, self.body.position)

        self.body.angular_velocity *= 0.5

    def launch(self, difference):
        """
        Launch the missile
        """
        power = max(min(difference, 1000), 10)
        impulse = power * Vec2d(1, 0)
        impulse.rotate(self.body.angle)

        # Apply force to the missile (launch the missile)
        self.body.apply_impulse_at_world_point(impulse, self.body.position)
        self.launched = True

    def ready_to_blit(self):
        """
        :return True if the missile is launched and has not collided with another shape
        """
        return self.launched and not self.collided
