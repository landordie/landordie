"""
AntiSpaceCraft class
"""
from classes.missile import Missile
from constants import *
import pymunk
from .sprite_class import Sprite


class AntiSpaceCraft:
    sf = pymunk.ShapeFilter(group=1)

    def __init__(self, mass=DEFAULT_MASS, position=(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 4)):
        self._fuel = 500
        self.force = DEFAULT_FORCE
        self.wheels = []
        # Anti-spacecraft wheels
        self.wheel1_b, self.wheel1_s = self.create_body(mass, (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                               position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheel2_b, self.wheel2_s = self.create_body(mass, (position[0] + ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                               position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        # self.wheel3_b, self.wheel3_s = self.create_body(mass, (position[0] - ANTI_SPACECRAFT_CHASSIS[0]/15,
        # position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheels.extend((self.wheel1_b, self.wheel2_b))  # , self.wheel3_b))

        # Anti-spacecraft chassis
        self.chassis_b, self.chassis_s = self.create_body(mass / 5, position, ANTI_SPACECRAFT_CHASSIS)
        self.chassis_s.color = 128, 128, 128

        # Create cannon
        self.cannon_b, self.cannon_s = self.create_body(0.01,
                                                        (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 2, position[1] +
                                                         ANTI_SPACECRAFT_CHASSIS[1] / 2), ANTI_SPACECRAFT_CANNON)
        self.cannon_s.color = (128, 128, 128)

        self.missile = Missile()
        self.body_sprite = Sprite("frames/tanker.png")
        self.cannon_sprite = Sprite("frames/cannon.png")

        # Anti-spacecraft joints
        # TODO: Use for-loop (?)
        self.pin1 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (-ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin2 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin3 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin4 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin5 = pymunk.PinJoint(self.wheel1_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin6 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin7 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin8 = pymunk.PinJoint(self.cannon_b, self.chassis_b, (ANTI_SPACECRAFT_CANNON[0] / 2, 0),
                                    (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        # self.pin9 = pymunk.PinJoint(self.wheel3_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        # self.pin10 = pymunk.PinJoint(self.wheel3_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1]))
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

    def fuel_bar(self, display, height):
        fuel = max(self.fuel, 0)
        # Red bar underneath to make the fuel drop visible
        pg.draw.line(display, RED, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] + 87,
                            self.chassis_b.position[1] - 45), height), 10)
        # Actual fuel bar
        pg.draw.line(display, GREEN, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] - 79 + fuel / 3,
                            self.chassis_b.position[1] - 45), height), 10)
