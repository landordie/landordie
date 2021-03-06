"""
'missile.py' module.
Used in creating the cannon missile body and shape.
"""
from math import pi, pow, degrees
import pymunk as pm
from pymunk.vec2d import Vec2d
from .constants import MISSILE_DRAG_CONSTANT
from .sprite_class import Sprite


class Missile(Sprite):
    """Missile Sprite subclass implementation."""

    def __init__(self):
        """Virtually private constructor which initializes the missile Sprite."""
        super().__init__('assets/frames/missile_small.gif')  # call Sprite initializer

        self.body, self.shape = None, None  # Pymunk body and shape of the missile
        self.launched = False  # Boolean to check if the missile has been launched
        self.collided = True  # Boolean to check if the missile has collided with another object

    def create(self, position):
        """
        Create new missile body and shape at specified location.
        :param position: new body and shape position coordinates
        """
        vs = [(-30, 0), (0, 3), (10, 0), (0, -3)]  # Polygon point coordinates
        mass = 0.5
        moment = pm.moment_for_poly(mass, vs)
        self.body = pm.Body(mass, moment)  # Create the body
        self.body.position = position  # Position the body
        self.shape = pm.Poly(self.body, vs)  # Create the shape
        self.shape.color = (115.0, 148.0, 107.0, 100.0)
        self.shape.friction = .5  # Set the shape friction with other objects
        self.shape.collision_type = 3
        self.shape.filter = pm.ShapeFilter(group=1)

    def prepare_for_launch(self, cannon_body, cannon_shape):
        """
        Position the missile for launch (at anti-spacecraft cannon location)
        :param cannon_body: anti-spacecraft cannon body
        :param cannon_shape: anti-spacecraft cannon shape
        """
        self.body.position = cannon_body.position + Vec2d(cannon_shape.radius - 30, 0).rotated(cannon_body.angle)
        self.body.angle = cannon_body.angle + pi

    def apply_gravity(self):
        """Apply gravitational effects to the launched missile."""
        pointing_direction = Vec2d(1, 0).rotated(self.body.angle)
        flight_direction = Vec2d(self.body.velocity)
        flight_speed = flight_direction.normalize_return_length()
        dot = flight_direction.dot(pointing_direction)

        # Calculate (roughly) the air resistance effect force on the missile
        drag_force_magnitude = (1 - abs(dot)) * pow(flight_speed, 2) * MISSILE_DRAG_CONSTANT * self.body.mass

        # Apply impulse to the missile body
        self.body.apply_impulse_at_world_point(drag_force_magnitude * -flight_direction, self.body.position)

        # Rotate missile simulating (roughly) air resistance
        if 90 <= degrees(self.body.angle) < 270:
            self.body.angular_velocity += .025
        elif 90 > degrees(self.body.angle) >= -90:
            self.body.angular_velocity -= .025
        else:
            self.body.angular_velocity = 0

    def launch(self, difference):
        """
        Calculate impulse strength and launch the missile.
        :param difference: the time between the 'shoot' key press and its release
        """
        power = max(min(difference, 1000), 10)
        impulse = power * Vec2d(1, 0)
        impulse.rotate(self.body.angle)

        # Apply force to the missile (launch the missile)
        self.body.apply_impulse_at_world_point(impulse, self.body.position)
        self.launched = True

    def ready_to_blit(self):
        """
        Check if the missile is ready to be shown on the screen
        :return True if the missile is launched and has not collided with another shape
        """
        return self.launched and not self.collided

    def remove_from_space(self, space):
        """
        Remove the body and shape of the missile and reset its attributes.
        :param space: Pymunk object space
        """
        space.remove(self.body)
        space.remove(self.shape)
        self.launched = False
        self.collided = True
