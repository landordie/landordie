import pygame


class Sprite(pygame.sprite.Sprite):
    """ Changing the Sprite class to work for our solution - to create static objects(background, obstacles, etc.)"""
    def __init__(self, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
