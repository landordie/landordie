"""
AntiSpaceCraft class
"""
from classes.missile import Missile
from constants import *
import pymunk
from .sprite_class import Sprite


class AntiSpaceCraft:
    """Anti-spacecraft vehicle instance class"""

    sf = pymunk.ShapeFilter(group=1)  # This shape filter object is responsible for making sure that all the parts of
    # the anti-spacecraft vehicle (chassis, wheels, cannon, joints) can overlap and do not collide with each other.

    def __init__(self, mass=DEFAULT_MASS, position=(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 4)):
        """
        Create all the body parts of (construct) the anti-spacecraft vehicle
        :param mass: default body mass
        :param position: default body position
        """
        self._fuel = 500  # A fuel indicator that decreases with movement
        self.force = DEFAULT_FORCE  # The default force that acts on the wheels of the vehicle
        self.wheels = []  # A list that manages the wheels (similar to a group)

        # Anti-spacecraft wheels
        self.wheel1_b, self.wheel1_s = self.create_body(ANTI_SPACECRAFT_WHEEL_MASS,
                                                        (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                         position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)
        self.wheel2_b, self.wheel2_s = self.create_body(ANTI_SPACECRAFT_WHEEL_MASS,
                                                        (position[0] + ANTI_SPACECRAFT_CHASSIS[0] / 1.5,
                                                         position[1]), ANTI_SPACECRAFT_WHEEL_SIZE)

        self.wheel3_b, self.wheel3_s = self.create_body(ANTI_SPACECRAFT_WHEEL_MASS, (position[0], position[1]),
                                                        ANTI_SPACECRAFT_WHEEL_SIZE)

        # Add all wheels to the wheels list (used for applying force to all of them with a for loop)
        self.wheels.extend((self.wheel1_b, self.wheel2_b, self.wheel3_b))

        # Anti-spacecraft chassis creation
        self.chassis_b, self.chassis_s = self.create_body(ANTI_SPACECRAFT_CHASSIS_MASS, position,
                                                          ANTI_SPACECRAFT_CHASSIS)
        self.chassis_s.color = DARK_GREY  # Set the anti-spacecraft chassis color

        # Create the cannon (pymunk body and shape)
        self.cannon_b, self.cannon_s = self.create_body(ANTI_SPACECRAFT_CANNON_MASS,
                                                        (position[0] - ANTI_SPACECRAFT_CHASSIS[0] / 2,
                                                         position[1] + ANTI_SPACECRAFT_CHASSIS[1] / 2),
                                                        ANTI_SPACECRAFT_CANNON)
        self.cannon_s.color = DARK_GREY  # Set the anti-spacecraft cannon color

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
        self.pin8 = pymunk.PinJoint(self.wheel3_b, self.chassis_b, (0, 0), (-ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin9 = pymunk.PinJoint(self.wheel3_b, self.chassis_b, (0, 0), (ANTI_SPACECRAFT_CHASSIS[0] / 2, 0))
        self.pin10 = pymunk.PinJoint(self.wheel2_b, self.chassis_b, (0, 0), (0, -ANTI_SPACECRAFT_CHASSIS[1] / 2))
        self.pin11 = pymunk.PinJoint(self.cannon_b, self.chassis_b, (ANTI_SPACECRAFT_CANNON[0] / 2, 0),
                                     (0, ANTI_SPACECRAFT_CHASSIS[1] / 2))
        # TODO:
        # self.pin1.color = self.pin2.color = self.pin3.color = self.pin4.color = self.pin5.color = self.pin6.color = \
        #     self.pin7.color = self.pin8.color = self.pin9.color = self.pin10.color = self.pin11.color = DARK_GREY
        # Create a simple motor for the cannon so it rotates around its pin joint
        self.cannon_mt = pymunk.SimpleMotor(self.cannon_b, self.chassis_b, 0)
        self.cannon_mt.collide_bodies = False

    @staticmethod
    def create_body(mass, position, shape_type, friction=TERRAIN_FRICTION):
        """
        Create Pymunk body and shape from given mass, position, shape type and friction
        :param mass: body mass
        :param position: body position
        :param shape_type: type of the shape to be created
        :param friction: shape friction
        :return: body and shape
        """
        body = pymunk.Body()
        body.mass = mass
        body.position = position
        if shape_type == ANTI_SPACECRAFT_WHEEL_SIZE:
            body.moment = pymunk.moment_for_circle(mass, 0, ANTI_SPACECRAFT_WHEEL_SIZE)
            shape = pymunk.Circle(body, ANTI_SPACECRAFT_WHEEL_SIZE)
            shape.color = DARK_GREY
        else:
            body.moment = pymunk.moment_for_box(mass, shape_type)
            shape = pymunk.Poly.create_box(body, shape_type)
        shape.friction = friction
        shape.filter = AntiSpaceCraft.sf  # Make sure all parts that are created have the same filter
        return body, shape

    def add_to_space(self, space):
        """
        Add all the parts (bodies and shapes) of the anti-spacecraft to the Pymunk space
        :param space: Pymunk space
        """
        # Add all the body parts of the anti-spacecraft to the Pymunk space
        space.add(self.wheel1_b, self.wheel1_s)
        space.add(self.wheel2_b, self.wheel2_s)
        space.add(self.wheel3_b, self.wheel3_s)
        space.add(self.chassis_b, self.chassis_s)
        space.add(self.cannon_b, self.cannon_s)
        space.add(self.pin1, self.pin2, self.pin3, self.pin4, self.pin5, self.pin6, self.pin7, self.pin9, self.pin11,
                  self.pin10)
        space.add(self.pin8, self.cannon_mt)

    def apply_force(self):
        """
        Apply the specified force on the wheels of the anti-spacecraft vehicle
        """
        for wheel in self.wheels:  # Apply same force on both wheels
            wheel.apply_force_at_local_point(self.force, wheel.position)

    def force_right(self):
        """
        Consume fuel and increase the force towards the positive direction of the x-axis. The change in the force will be
        reflected in the apply_force() method above, as it is called and updated every frame
        """
        self.fuel -= 1
        self.force = (ANTI_SPACECRAFT_MOVE_FORCE, 0)

    def force_left(self):
        """
        Consume fuel and increase the force towards the negative direction of the x-axis.
        """
        self.fuel -= 1
        self.force = (-ANTI_SPACECRAFT_MOVE_FORCE, 0)

    @property
    def fuel(self):
        """
        Getter method for the fuel attribute
        :return: fuel attribute
        """
        return self._fuel

    @fuel.setter
    def fuel(self, f):
        """
        Setter method for the fuel attribute
        :param f: fuel amount
        """
        self._fuel = f

    def fuel_bar(self, display, height):
        """
        Display the changes to the fuel level on the screen.
        It creates a green bar which decreases as fuel drops and the missing green part is substituted by red color.
        :param display: surface of the screen
        :param height: height of the current scene window
        """
        fuel = max(self.fuel, 0)
        # Red bar underneath to make the fuel drop visible
        pg.draw.line(display, RED, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] + 87,
                            self.chassis_b.position[1] - 45), height), 10)
        # Actual fuel bar
        pg.draw.line(display, GREEN, flipy((self.chassis_b.position - (80, 45)), height),
                     flipy((self.chassis_b.position[0] - 79 + fuel / 3,
                            self.chassis_b.position[1] - 45), height), 10)
