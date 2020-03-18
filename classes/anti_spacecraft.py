"""
AntiSpaceCraft class
"""
from classes.missile import Missile
from constants import *
import pymunk
from .sprite_class import Sprite


class AntiSpaceCraft:
    sf = pymunk.ShapeFilter(group=1)  # This shape filter object is responsible for making sure that all the parts of
    # the anti-spacecraft vehicle (chassis, wheels, cannon, joints) can overlap and do not collide with each other.

    def __init__(self, mass=DEFAULT_MASS, position=(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 4)):
        # The initialized of this class creates all the body parts of the gunned vehicle
        self._fuel = 500  # A fuel indicator that decreases with movement
        self.force = DEFAULT_FORCE  # The default force that acts on the wheels of the vehicle
        self.wheels = []  # A list that manages the wheels (similar to a group)

        # Anti-spacecraft wheels
        self.wheel1_b, self.wheel1_s = self.create_body(mass, (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                               position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheel2_b, self.wheel2_s = self.create_body(mass, (position[0] + ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                               position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        # Add all wheels to the list
        self.wheels.extend((self.wheel1_b, self.wheel2_b))

        # Anti-spacecraft chassis creation
        self.chassis_b, self.chassis_s = self.create_body(mass / 5, position, ANTI_SPACECRAFT_CHASSIS)
        self.chassis_s.color = 128.0, 128.0, 128.0, 255.0

        # Create cannon
        self.cannon_b, self.cannon_s = self.create_body(0.01,
            (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 2,
             position[1] + ANTI_SPACECRAFT_CHASSIS[1] / 2), ANTI_SPACECRAFT_CANNON)
        self.cannon_s.color = (128.0, 128.0, 128.0, 255.0)

        self.missile = Missile()  # Initialize the missile (creates both the pygame and pymunk missile representations)
        self.body_sprite = Sprite("frames/tanker.png")  # Sprite for the body (a tank image)
        self.cannon_sprite = Sprite("frames/cannon.png")  # Sprite for the cannon

        # Anti-spacecraft joints which are used to connect all the components together with wires.
        # These connections ensure the flexibility of the vehicle during collisions and slope conquering
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

        # Create a simple motor for the cannon so it rotates around its pin joint
        self.cannon_mt = pymunk.SimpleMotor(self.cannon_b, self.chassis_b, 0)
        self.cannon_mt.collide_bodies = False

    @staticmethod
    # This static method is used to create pymunk body and shapes from given mass, position, friction and shape type
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
        shape.filter = AntiSpaceCraft.sf  # Make sure all parts that are created have the same filter
        return body, shape

    def apply_force(self):
        # This method applies the specified force on the wheels of the vehicle
        for wheel in self.wheels:  # Apply same force on both wheels
            wheel.apply_force_at_local_point(self.force, wheel.position)

    def force_right(self):
        # Consume fuel and increase the force along the POSITIVE x axis. Then this change in the force will be reflected
        # in the apply_force() method above, as it is called and updated every frame
        self.fuel -= 1
        self.force = (ANTI_SPACECRAFT_MOVE_FORCE, 0)

    def force_left(self):
        # Consume fuel and increase the force along the NEGATIVE x axis.
        self.fuel -= 1
        self.force = (-ANTI_SPACECRAFT_MOVE_FORCE, 0)

    @property
    def fuel(self):
        # A getter method for the fuel attribute
        return self._fuel

    @fuel.setter
    def fuel(self, f):
        self._fuel = f

    def fuel_bar(self, display, height):
        # This method is responsible for displaying the changes to the fuel level on the screen.
        # It creates a green bar which decreases as fuel drops and the missing green part is substituted by red color
        fuel = max(self.fuel, 0)
        # Red bar underneath to make the fuel drop visible
        pg.draw.line(display, RED, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] + 87,
                            self.chassis_b.position[1] - 45), height), 10)
        # Actual fuel bar
        pg.draw.line(display, GREEN, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] - 79 + fuel / 3,
                            self.chassis_b.position[1] - 45), height), 10)
