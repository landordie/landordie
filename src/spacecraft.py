"""
'spacecraft.py' module.
Used in instantiating the game spacecraft.
"""
import pymunk
from math import degrees, sqrt, pow, radians
from .constants import *
from .sprite_class import Sprite
from .helper import flipy, draw_text


class Spacecraft(Sprite):
    """Spacecraft instance subclass implementation."""

    def __init__(self):
        # Call the Sprite initializer (this creates an image surface object, a Rectangle object
        # and provides the 'get_attachment_coordinates() method)
        super().__init__('assets/frames/lander.gif')

        # This variable holds the rotated image if the lander is being rotated or the original
        # image by default
        self.normal = self.image
        
        # This variable holds the image for the case when thrust is applied and must appear.
        # The original is swapped with this image every time the activate engine button is
        # pressed on keyboard
        self.activated_img = pg.image.load("assets/frames/lander_active.png")
        
        # This method takes the actual size of the image ignoring its transparent parts
        self.mask = pg.mask.from_surface(self.image)

        # Initializing lander's attributes: the health, the damage percentage,
        # terrain collision cooldown and boolean to account for collision
        self.health = 100
        self.damage = 0
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

        self.health_bar_img = pg.image.load("assets/frames/heart.png")  # Load the health bar image
        self.velocity = 0  # Spacecraft velocity attribute
        self.flicker_time = 90  # Used when displaying the malfunction text (90 frames or 1.5 seconds)

    def health_bar(self, display, height):
        """
        Draw the health bar, its border and heart icon.
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

        # Draw the health bar border
        x, y = flipy((self.body.position - (80, 45)), height)
        pg.draw.rect(display, BLACK, (x, y-5, 157, 12), 3)  # width = 3

        # Display the health bar heart icon
        display.blit(self.health_bar_img, flipy((self.body.position - (100, 45)),
                                                height - self.health_bar_img.get_size()[1] // 2))

    def rotate_left(self):
        """Rotate the spacecraft body to the left."""
        self.body.angle += radians(2)

    def rotate_right(self):
        """Rotate the spacecraft body to the right."""
        self.body.angle -= radians(2)

    def malfunction(self):
        """
        Start malfunctioning (random side rotation) on boundary contact or hard landing attempt
        if the spacecraft drops below half health.
        """
        if self.health >= 50:
            self.body.angular_velocity = 0
            return False
        return True

    def crashed(self):
        """
        Return True if the spacecraft's health has dropped to 0 or below.
        :return: boolean
        """
        return self.health <= 0

    def show_stats(self, display, position):
        """
        Display the velocity, body angle of the spacecraft and malfunction text.
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
        draw_text(display, f"{self.velocity}", (position[0] + 70, position[1] + 30), FONT_SMALL, YELLOW)
        draw_text(display, f"{abs(int(degrees(self.body.angle))) % 360}", (position[0] + 35, position[1] + 60),
                  FONT_SMALL, YELLOW)

        if self.malfunction():  # Check if spacecraft is prone to malfunctioning
            self.flicker_time -= 1  # Decrement the time
            if 90 >= self.flicker_time > 0:  # Show the text for 1.5 seconds
                draw_text(display, "*SYSTEM MALFUNCTION*", (position[0] + 50, position[1] + 90), FONT_SMALLEST, RED)
            elif self.flicker_time <= 0:  # Reset the malfunction text flicker time to 3 seconds
                self.flicker_time = 180

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
