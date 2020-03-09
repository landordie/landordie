import pygame
import random
from constants import *

""" Credits: https://gist.github.com/ogilviemt/9b05a89d023054e6279f"""

class StarField:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []
        self.initialize_stars()

    def set_params(self, width, height):
        self.width = width
        self.height = height

    def initialize_stars(self):
        for slow_stars in range(50):  # birth those plasma balls, baby
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_slow.append([star_loc_x, star_loc_y])  # i love your balls

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.width)
            star_loc_y = random.randrange(0, self.height)
            self.star_field_fast.append([star_loc_x, star_loc_y])

    def draw_stars(self, screen):
        for star in self.star_field_slow:
            star[1] += 1
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, DARK_GREY, star, 3)

        for star in self.star_field_medium:
            star[1] += 4
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, LIGHT_GREY, star, 2)

        for star in self.star_field_fast:
            star[1] += 8
            if star[1] > self.height:
                star[0] = random.randrange(0, self.width)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(screen, YELLOW, star, 1)
