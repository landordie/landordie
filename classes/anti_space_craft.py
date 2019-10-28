"""
AntiSpaceCraft class
"""
from constants import *
import pymunk


class AntiSpaceCraft:
    sf = pymunk.ShapeFilter(group=1)

    def __init__(self, mass=DEFAULT_MASS, moment=DEFAULT_MOMENT, position=(G_SCREEN_WIDTH/4, G_SCREEN_HEIGHT/4)):
        self.force = DEFAULT_FORCE
        self.wheels = []

        # Anti-spacecraft wheels
        self.wheel1_b, self.wheel1_s = self.create_body(mass, moment, (position[0] - ANTI_SPACECRAFT_CHASSIS[0]/1.5,
                                                                       position[1]), 'wheel')

        self.wheel2_b, self.wheel2_s = self.create_body(mass, moment, (position[0] + ANTI_SPACECRAFT_CHASSIS[0]/1.5,
                                                                       position[1]), 'wheel')
        # Anti-spacecraft chassis
        self.chassis_b, self.chassis_s = self.create_body(mass/5, moment, position, 'chassis')
        self.chassis_s.color = 255, 155, 0

        self.cannon_b, self.cannon_s = self.create_body(0.01, 0.1, (position[0] - ANTI_SPACECRAFT_CHASSIS[0]/2, position[1]), 'cannon')
        self.cannon_s.filter = pymunk.ShapeFilter(group=2)
        # self.cannon_b.body_type = pymunk.Body.KINEMATIC
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
        self.cannon_mt = pymunk.SimpleMotor(self.cannon_b,self.chassis_b, 0);

    def create_body(self, mass, moment, position, shape_type, friction=DEFAULT_FRICTION):
        body = pymunk.Body(mass, moment)
        body.position = position
        if shape_type.lower() == 'wheel':
            self.wheels.append(body)
            shape = pymunk.Circle(body, ANTI_SPACECRAFT_WHEEL_SIZE)
        elif shape_type.lower() == 'chassis':
            shape = pymunk.Poly.create_box(body, ANTI_SPACECRAFT_CHASSIS)
        else:
            shape = pymunk.Poly.create_box(body, ANTI_SPACECRAFT_CANNON)
        shape.friction = friction
        shape.filter = AntiSpaceCraft.sf
        return body, shape

    def apply_force(self):
        for wheel in self.wheels:
            wheel.apply_force_at_local_point(self.force, wheel.position)

    def force_right(self):
        self.force = (ANTI_SPACECRAFT_MOVE_FORCE, 0)

    def force_left(self):
        self.force = (-ANTI_SPACECRAFT_MOVE_FORCE, 0)
