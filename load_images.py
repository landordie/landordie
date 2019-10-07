import pygame
import os


def load_images(path_to_directory):
    """Load images and return them as a dict."""
    image_dict = {}
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.gif'):
            path = os.path.join(path_to_directory, filename)
            key = filename[:-4]
            image_dict[key] = pygame.image.load(path).convert()
    return image_dict


def update(surfaces, screen):
    w, h = screen.get_surface().get_width(), screen.get_surface().get_height()
    for surface in surfaces:
        #screen.get_surface().blit(surface, (w / 2 - 250, h / 4))
        screen.get_surface().blit(surface, (w / 2 - 350, 50))
        screen.update()

"""   Example:
Load the images in a dictionary - (key:value => image_name:pygame.Surface_object) 
    image_frames = load_images("frames/medium")
Create a list containing all the surfaces
    pygame_surfaces = image_frames.values()

Blitting images on the screen using for loop:
    for surface in pygame_surfaces:
    
After each blit add a delay "pygame.time.Clock().delay(60)" for best performance
        display.blit(surf, (w / 2 - 250, h / 4))
        py_time.delay(60)
    
Update the display after each blit
        pygame.display.update()
"""


