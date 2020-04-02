"""
'spacecraft.py' module.
Used in instantiating the game spacecraft.
"""
import pymunk
from math import degrees, sqrt, pow
from constants import *
from .sprite_class import Sprite
from .helper import flipy, draw_text


class Spacecraft(Sprite):
    """Spacecraft instance subclass."""

    def __init__(self):
        # Call the Sprite initializer (this creates an image surface object, a Rectangle object
        # and provides the 'get_attachment_coordinates() method)
        super().__init__('frames/lander.gif')

        # This variable holds the rotated image if the lander is being rotated or the original
        # image by default
        self.normal = self.image
        
        # This variable holds the image for the case when thrust is applied and must appear.
        # The original is swapped with this image every time the activate engine button is
        # pressed on keyboard
        self.activated_img = pg.image.load("frames/lander_active.png")
        
        # This method takes the actual size of the image ignoring its transparent parts
        self.mask = pg.mask.from_surface(self.image)

        # Initializing lander's attributes: the health, the damage percentage, boolean attribute
        # to reflect if crashed, terrain collision cooldown and boolean to account for collision
        self.health = 100
        self.damage = 0
        self.crashed = False
        self.terrain_collision_cd = 0
        self.terrain_collision = True

        # Initializing the pymunk representation of the space craft. The list of vertices is used by
        # Pymunk to create the shape of the spacecraft body. Each tuple in the list is a coordinate of
        # a point. Linking all points creates the shape. Then we initialize the mass, moment, Body and
        # Shape objects. We set the friction that acts on the craft and adjust its color and collision
        # type. Lastly, we position the spacecraft.
        self.polygon_vertices = [(-30, -25), (30, -25), (0, 35)]
        self.mass = 0.6
        self.moment = pymunk.moment_for_poly(self.mass, self.polygon_vertices)
        self.body = pymunk.Body(self.mass, self.moment)
        self.shape = pymunk.Poly(self.body, self.polygon_vertices)
        self.shape.friction = 1
        self.shape.color = BLACK_INVISIBLE
        self.shape.collision_type = 2  # Set the shape collision type for the collision handler
        self.body.position = 600, 700

        self.health_bar_img = pg.image.load("frames/heart.png")  # Load the health bar image
        self.velocity = 0

    def health_bar(self, display, height):
        """
        Draw the health bar.
        :param display: current scene screen surface
        :param height: current scene height
        """

        # Dark red bar underneath to make the health drop visible
        pg.draw.line(display, (156, 12, 12), flipy((self.body.position - (80, 45)), height),
                     flipy((self.body.position[0] + 75,
                            self.body.position[1] - 45), height), 10)

        # Actual health bar (red)
        pg.draw.line(display, RED, flipy((self.body.position - (80, 45)), height),
                     flipy((self.body.position[0] + 75 - self.damage,
                            self.body.position[1] - 45), height), 10)

        x, y = flipy((self.body.position - (80, 45)), height)
        pg.draw.rect(display, BLACK, (x, y-5, 157, 12), 3)  # width = 3

        display.blit(self.health_bar_img, flipy((self.body.position - (100, 45)),
                                                height - self.health_bar_img.get_size()[1] // 2))

    def show_stats(self, display, position):
        """
        Display the velocity and body angle of the spacecraft.
        :param display: Pygame screen surface
        :param position: on-screen position of the texts
        """
        # Display the spacecraft stats indicators
        indicators = ["Spacecraft", "Velocity: ", "Angle:    "]
        for i in range(len(indicators)):
            current_ind = indicators[i]
            draw_text(display, current_ind, (position[0], position[1] + i*30), FONT_SMALL, CYAN)

        # Calculate and display the velocity and spacecraft body angle
        x_velocity, y_velocity = self.body.velocity
        self.velocity = int(sqrt(pow(x_velocity, 2) + pow(y_velocity, 2)) // 50)
        draw_text(display, f"{self.velocity}", (position[0] + 60, position[1] + 30),
                  FONT_SMALL, YELLOW)
        draw_text(display, f"{abs(int(degrees(self.body.angle))) % 360}", (position[0] + 35, position[1] + 60),
                  FONT_SMALL, YELLOW)

    def apply_thrust(self):
        """Apply thrust force to the spacecraft (make it fly)."""
        self.body.apply_impulse_at_local_point((self.body.angle, 20))  # Generate and apply an impulse
        self.image = self.activated_img  # Swap the current image with the activated for the blit() method

    def receive_damage(self, dmg):
        """
        Decrease health by damage given.
        :param dmg: damage amount
        """
        self.health -= dmg  # Decrease health
        self.damage += dmg * 1.5  # This variable is used in the health bar, to ensure that it decreases properly

    def get_landing_condition(self):
        """
        Check spacecraft-related landing conditions. Called every time the spacecraft collides with the
        landing pad sprite. On such a collision the health of the spacecraft must be more than 0, its
        rotation angle must be at max 10 in both directions and its falling velocity must be less than
        300 pixels per sec.
        """
        return self.health > 0 and abs(degrees(self.body.angle)) % 360 <= 10 and self.velocity <= 5
