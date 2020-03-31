"""
'star_field.py' module.
Used in creating a dynamic (moving dots (stars)) background image instance.
Credits: https://gist.github.com/ogilviemt/9b05a89d023054e6279f
"""
import pygame
import random
from constants import *


class StarField:
    """StarField class implementation."""

    def __init__(self, width, height):
        """
        Virtually private constructor which initializes a dynamic
        background image instance.
        :param width:
        :param height:
        """
        self.width = width  # Get the width of the dynamic background field
        self.height = height  # Get the height of the dynamic background field
        self.star_field_slow = []  # Stores the slow layer dots' coordinates
        self.star_field_medium = []  # Stores the medium layer dots' coordinates
        self.star_field_fast = []  # Stores the fast layer dots' coordinates
        self.initialize_stars()  # Call the dynamic background layer initializer

    def set_params(self, width, height):
        """Screen width and height setter method."""
        self.width = width
        self.height = height

    def initialize_stars(self):
        """
        Generate the dynamic background in three layers:
        slow, medium and fast moving white dots.
        """
        for slow_stars in range(50):  # 50 slow speed white dots
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(35):  # 35 medium speed white dots
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):  # 15 fast speed white dots
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_fast.append([star_loc_x, star_loc_y])

    def draw_stars(self, screen):
        """
        Draw the three-layered dynamic background on the screen.
        :param screen: the Pygame display
        """
        for star in self.star_field_slow:
            # Change the y-axis coordinate of the dot to achieve
            # the downward movement effect
            star[1] += 1
            # On dots reaching the bottom of the screen
            # randomize the dots and spawn from top
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, DARK_GREY, star, 3)

        for star in self.star_field_medium:
            # Change the y-axis coordinate of the dot to achieve
            # the downward movement effect
            star[1] += 4
            # On dots reaching the bottom of the screen
            # randomize the dots and spawn from top
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, LIGHT_GREY, star, 2)

        for star in self.star_field_fast:
            # Change the y-axis coordinate of the dot to achieve
            # the downward movement effect
            star[1] += 8
            # On dots reaching the bottom of the screen
            # randomize the dots and spawn from top
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, YELLOW, star, 1)
