import pygame
from PyMunk.classes.button import *
from PyMunk.load_images import load_images
from PyMunk.load_images import update as title_update


# (!) REMEMBER (!)
# When changing scenes, resolution is hardcoded
#


# Tuple unpacking for text display
def __text_objects(text, font):
    surface = font.render(text, True, BLACK)
    return surface, surface.get_rect()


# Method used to display text
# It's used on multiple occasions that's why it's taken out as a separate method
# Args: screen -> pygame.display object
#       text -> string you want displayed
#       size -> the size of the string (different lengths need different size)
#       font -> name of the font
def displayText(screen, text, font, size):
    screen = screen.get_surface()
    width, height = screen.get_size()
    font = pygame.font.Font(font, size)
    surface, rect = __text_objects(text, font)
    rect.center = ((width / 2), (height / 4))
    screen.blit(surface, rect)
    pygame.display.update()


class SceneBase:
    def __init__(self):
        self.next = self

    # Using this method mainly for testing
    # The game logic will be implemented in the Update() method
    def ProcessInput(self, events, pressed_keys):
        print("(!) Override in child class (!)")

    def Update(self):
        print("(!) Override in child class (!)")

    def Render(self, screen):
        print("(!) Override in child class (!)")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)


class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pg.mixer.Sound("blipshort1.wav").play()

    def Update(self):
        pass

    @staticmethod
    def scene_wh(screen):
        """
        Scene width and height
        """
        width = screen.get_surface().get_width()
        height = screen.get_surface().get_height()
        return width, height

    # (!) When adding buttons to the start screen
    # (!) Add them here, in this method
    def Render(self, screen):

        # Width and height unpacking
        w, h = TitleScene.scene_wh(screen)

        # Start and Quit buttons
        menu_button = Button((w / 2 - (BUTTON_WIDTH/2), h / 2, BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW, 'Start')
        menu_button_2 = Button((w / 2 - (BUTTON_WIDTH/2), h / 1.5, BUTTON_WIDTH, BUTTON_HEIGHT), RED, 'Quit')

        game_title = load_images("frames/big")
        title_surfaces = game_title.values()

        screen.get_surface().fill(BLACK)

        # Update buttons
        menu_button.update(screen.get_surface())
        menu_button_2.update(screen.get_surface())

        # Update title
        title_update(title_surfaces, screen)
        # displayText(screen, "Land or Die", 'freesansbold.ttf', 75)


class GameScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(WinScene())
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                self.SwitchToScene(LoseScene())

    def Update(self):
        pass

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.set_mode((G_SCREEN_WIDTH, G_SCREEN_HEIGHT))
        screen.get_surface().fill(BLUE)


class WinScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((800, 600))
        screen.get_surface().fill(GREEN)
        displayText(screen, "Congratulations!"
                            "You have won!", 'freesansbold.ttf', 50)


class LoseScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((800, 600))
        screen.get_surface().fill(RED)
        displayText(screen, "Too bad! You have lost!", 'freesansbold.ttf', 45)
