from math import sin, cos, degrees
import pygame as pg
import pymunk as pm
from pymunk import Vec2d

# Example code for "spacecraft" taken from
# https://stackoverflow.com/questions/45909318/show-pymunk-with-pygame-python?fbclid=IwAR3wzLycH18U7kQlL3HTjiMDbSuAw3bB3KPhClr0i8RY06KDHEUFfMYez-o
def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Spacecraft(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.crashed = False
        # Drawing the shape
        self.image = pg.Surface((46, 52), pg.SRCALPHA)
        pg.draw.polygon(self.image, (0, 50, 200),
                        [(0, 0), (48, 0), (48, 54), (24, 54)])
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        # The vertices of the shape
        vs = [(-23, 26), (23, 26), (23, -26), (0, -26)]
        mass = 0.4
        moment = pm.moment_for_poly(mass, vs)
        # Attaching the shape to a body
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vs)
        self.shape.collision_type = 3
        self.body.position = pos

    # Like the update method in the Scenes(), this update is called every frame
    # and checks if rotation has been applied, if so it rotates the image(body/shape)
    def update(self):
        pos = flipy(self.body.position)
        self.rect.center = pos
        self.image = pg.transform.rotate(
            self.orig_image, degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    # Used to apply force to rotate the ship to the left
    def rotate_left(self):
        self.body.angular_velocity = 0.5

    # Used to apply force to rotate the ship to the right
    def rotate_right(self):
        self.body.angular_velocity = -0.5

    def move_up(self):
        """ This method helps the ship to counter-react the gravitation effect of the planet """
        self.body.apply_impulse_at_local_point(Vec2d(0, 15))
