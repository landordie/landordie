from .sprite_class import Sprite


# TODO implement this if necessary
class Thruster(Sprite):

    def __init__(self):
        super().__init__('frames/ogan.png')  # call Sprite initializer
        self.activated_image = Sprite("frames/ogan2.png")
