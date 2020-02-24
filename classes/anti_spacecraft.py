"""
AntiSpaceCraft class
"""
from constants import *
import pymunk


class AntiSpaceCraft:
    sf = pymunk.ShapeFilter(group=1)

    def __init__(self, mass=DEFAULT_MASS, position=(G_SCREEN_WIDTH/2, G_SCREEN_HEIGHT/4)):
        self._fuel = 500
        self.force = DEFAULT_FORCE
        self.wheels = []
        self.flying_missiles = []

        # Anti-spacecraft wheels
        self.wheel1_b, self.wheel1_s = self.create_body(mass, (position[0] - ANTI_SPACECRAFT_CHASSIS[0]/1.5,
                                                                       position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheel2_b, self.wheel2_s = self.create_body(mass, (position[0] + ANTI_SPACECRAFT_CHASSIS[0]/1.5,
                                                                       position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheels.extend((self.wheel1_b, self.wheel2_b))

        # Anti-spacecraft chassis
        self.chassis_b, self.chassis_s = self.create_body(mass/5, position, ANTI_SPACECRAFT_CHASSIS)
        self.chassis_s.color = 255, 155, 0

        # Create cannon
        self.cannon_b, self.cannon_s = self.create_body(0.01, (position[0] - ANTI_SPACECRAFT_CHASSIS[0]/2, position[1] +
                                                               ANTI_SPACECRAFT_CHASSIS[1]/2), ANTI_SPACECRAFT_CANNON)

        # TODO: attach missile sprite, make it rotate and check for collision
        self.missile = pg.image.load("frames/missile.gif")
        self.m_rect = self.missile.get_rect()
        #####################################

        self.missile_body, self.missile_shape = self.create_missile()

        # Anti-spacecraft joints
        # TODO: Use for-loop (?)
        self.pin1 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (-ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin2 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin3 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin4 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin5 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin6 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin7 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin8 = pymunk.PinJoint(self.cannon_b, self.chassis_b, (ANTI_SPACECRAFT_CANNON[0]/2, 0), (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.cannon_mt = pymunk.SimpleMotor(self.cannon_b, self.chassis_b, 0)
        self.cannon_mt.collide_bodies = False

    @staticmethod
    def create_body(mass, position, shape_type, friction=TERRAIN_FRICTION):
        body = pymunk.Body()
        body.mass = mass
        body.position = position
        if shape_type == ANTI_SPACECRAFT_WHEEL_SIZE:
            body.moment = pymunk.moment_for_circle(mass, 0, ANTI_SPACECRAFT_WHEEL_SIZE)
            shape = pymunk.Circle(body, ANTI_SPACECRAFT_WHEEL_SIZE)
        else:
            body.moment = pymunk.moment_for_box(mass, shape_type)
            shape = pymunk.Poly.create_box(body, shape_type)
        shape.friction = friction
        shape.filter = AntiSpaceCraft.sf
        return body, shape

    @staticmethod
    def create_missile():
        vs = [(-30, 0), (0, 3), (10, 0), (0, -3)]
        mass = 0.5
        moment = pymunk.moment_for_poly(mass, vs)
        missile_body = pymunk.Body(mass, moment)

        missile_shape = pymunk.Poly(missile_body, vs)
        missile_shape.friction = .5
        missile_shape.collision_type = 2
        missile_shape.filter = AntiSpaceCraft.sf
        return missile_body, missile_shape

    def is_collided_with(self, sprite):
        return self.missile_body.position == sprite.position

    def apply_force(self):
        for wheel in self.wheels:
            wheel.apply_force_at_local_point(self.force, wheel.position)

    def force_right(self):
        self.fuel -= 1
        self.force = (ANTI_SPACECRAFT_MOVE_FORCE, 0)

    def force_left(self):
        self.fuel -= 1
        self.force = (-ANTI_SPACECRAFT_MOVE_FORCE, 0)

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, f):
        self._fuel = f
