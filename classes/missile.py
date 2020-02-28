import pygame
from .sprite_class import Sprite


# TODO implement this if necessary
class Missile(Sprite):

    def __init__(self):
        super().__init__('frames/missile.gif')  # call Sprite initializer
