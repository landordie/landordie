from classes import MenuScene
from classes.input_box import InputBox
from .game_scene import *
from .button import Button
import pygame


class OptionsScene(SceneBase):
    __instance = None
    controls = []

    @staticmethod
    def getInstance():
        """ Static access method. """
        if OptionsScene.__instance is None:
            OptionsScene()
        return OptionsScene.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if OptionsScene.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            OptionsScene.__instance = self

        SceneBase.__init__(self)
        self.background = pygame.image.load("frames/BG.png")
        self.x = 0
        self.input_boxes = []

        self.menu_button = Button(
            (self.screen_width * 0.2, self.screen_height * 0.8, BUTTON_WIDTH, BUTTON_HEIGHT),
            YELLOW,
            'Main Menu')

        """Containers"""
        self.res_cont_w, self.res_cont_h = self.screen_width / 5, self.screen_height / 3
        self.res_cont_x, self.res_cont_y = (self.screen_width / 2) - (self.res_cont_w * 2.26), \
                                           (self.screen_height / 2) - (self.res_cont_h / 2.35)
        self.res_cont = pygame.Surface((self.res_cont_w, self.res_cont_h)).convert_alpha()
        self.res_cont.fill(BLACK_HIGHLIGHT2)

        self.button_cont_w, self.button_cont_h = self.screen_width / 3, self.screen_height / 1.5
        self.button_cont_x, self.button_cont_y = (self.screen_width / 2), (self.screen_height / 5)
        self.button_cont = pygame.Surface((self.button_cont_w, self.button_cont_h)).convert_alpha()
        self.button_cont.fill(BLACK_HIGHLIGHT2)

        # TODO: Make the position of buttons be relative to container and not screen width/height

        self._res2 = Button(
            (self.res_cont_w / 3, self.res_cont_h / 0.85, BUTTON_WIDTH, BUTTON_HEIGHT),
            GREEN, "1280x800")
        self._res3 = Button(
            (self.res_cont_w / 3, self.res_cont_h / 0.62, BUTTON_WIDTH, BUTTON_HEIGHT),
            GREEN, "1440x900")

        self.input_box1 = InputBox(self.button_cont_x * 1.5, self.button_cont_y * 1.35, 'A')
        self.input_box2 = InputBox(self.button_cont_x * 1.5, self.button_cont_y * 1.60, 'W')
        self.input_box3 = InputBox(self.button_cont_x * 1.5, self.button_cont_y * 1.85, 'D')

        self.input_box4 = InputBox(self.button_cont_x * 1.45, self.button_cont_y * 2.75, 'Left')
        self.input_box5 = InputBox(self.button_cont_x * 1.45, self.button_cont_y * 3, 'Up')
        self.input_box6 = InputBox(self.button_cont_x * 1.45, self.button_cont_y * 3.25, 'Right')
        self.input_box7 = InputBox(self.button_cont_x * 1.45, self.button_cont_y * 3.5, 'Down')
        self.input_box8 = InputBox(self.button_cont_x * 1.45, self.button_cont_y * 3.75, 'Space')
        self.input_boxes = [self.input_box1, self.input_box2, self.input_box3, self.input_box4, self.input_box5,
                            self.input_box6, self.input_box7, self.input_box8]

    def ProcessInput(self, events, pressed_keys):
        for event in events:

            for input_box in self.input_boxes:
                input_box.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.Terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScene())
            """
            Handling changing of resolution
            """
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res2.on_click(event):
                _res = self._res2._text.split("x")
                SceneBase.screen_width, SceneBase.screen_height = int(_res[0]), int(_res[1])
                self.update_all()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res3.on_click(event):
                _res = self._res3._text.split("x")
                SceneBase.screen_width, SceneBase.screen_height = int(_res[0]), int(_res[1])
                self.update_all()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                # Pass input box texts
                menu = MenuScene.getInstance()
                menu.update_all()
                self.SwitchToScene(menu)

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))

        # Background parallax effect
        image_width = self.background.get_rect().width
        rel_x = self.x % image_width
        screen.get_surface().blit(self.background, (rel_x - image_width, 0))
        if rel_x < self.screen_width:
            screen.get_surface().blit(self.background, (rel_x, 0))
        self.x -= 1

        """Drawing the containers and displaying info text"""
        screen.get_surface().blit(self.res_cont, (self.res_cont_x, self.res_cont_y, self.res_cont_w, self.res_cont_h))
        self.draw_text(screen, "Resolution", (self.res_cont_x + self.res_cont_w / 2, self.res_cont_y / 1.1),
                       self.font_medium, WHITE)

        screen.get_surface().blit(self.button_cont,
                                  (self.button_cont_x, self.button_cont_y, self.button_cont_w, self.button_cont_h))
        self.draw_text(screen, "Controls", (self.button_cont_x + self.button_cont_w // 2, self.button_cont_y // 1.1),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Spacecraft", (self.button_cont_x + self.button_cont_w / 2, self.button_cont_y * 1.2),
                       self.font_medium, WHITE)
        self.draw_text(screen, "Anti-Spacecraft",
                       (self.button_cont_x + self.button_cont_w / 2, self.button_cont_y * 2.6),
                       self.font_medium, WHITE)

        self.draw_text(screen, "Thrust", (self.input_box1.rect.x * 0.8, self.input_box2.rect.y * 1.08),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Rotate Left", (self.input_box1.rect.x * 0.8, self.input_box1.rect.y * 1.08),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Rotate Right", (self.input_box1.rect.x * 0.8, self.input_box3.rect.y * 1.08),
                       self.font_medium, LIGHT_GREY)

        self.draw_text(screen, "Move Left", (self.input_box4.rect.x * 0.85, self.input_box4.rect.y * 1.04),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Cannon Right", (self.input_box5.rect.x * 0.85, self.input_box5.rect.y * 1.04),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Move Right", (self.input_box6.rect.x * 0.85, self.input_box6.rect.y * 1.04),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Cannon Left", (self.input_box7.rect.x * 0.85, self.input_box7.rect.y * 1.04),
                       self.font_medium, LIGHT_GREY)
        self.draw_text(screen, "Shoot", (self.input_box8.rect.x * 0.85, self.input_box8.rect.y * 1.04),
                       self.font_medium, LIGHT_GREY)

        self.menu_button.update(screen.get_surface())
        self._res2.update(screen.get_surface())
        self._res3.update(screen.get_surface())

        for input_box in self.input_boxes:
            input_box.draw(screen.get_surface())
            input_box.update()

    def update_all(self):
        """Reposition all buttons/containers when changing resolutions"""
        # The button that returns to Main Menu
        self.menu_button.rect.x, self.menu_button.rect.y = self.screen_width * 0.2, self.screen_height * 0.8

        # The two containers
        self.res_cont_w, self.res_cont_h = self.screen_width / 5, self.screen_height / 3
        self.res_cont_x, self.res_cont_y = (self.screen_width / 2) - (self.res_cont_w * 2.26), \
                                           (self.screen_height / 2) - (self.res_cont_h / 2.35)

        self.button_cont_w, self.button_cont_h = self.screen_width / 3, self.screen_height / 1.5
        self.button_cont_x, self.button_cont_y = (self.screen_width / 2), (self.screen_height / 5)
        self.button_cont = pygame.Surface((self.button_cont_w, self.button_cont_h)).convert_alpha()

        # The two buttons for resolutions
        self._res2.rect.x, self._res2.rect.y = self.res_cont_w / 3, self.res_cont_h / .85
        self._res3.rect.x, self._res3.rect.y = self.res_cont_w / 3, self.res_cont_h / .62
        self.res_cont = pygame.Surface((self.res_cont_w, self.res_cont_h)).convert_alpha()

        position_fractions = [[1.5, 1.5, 1.5, 1.45, 1.45, 1.45, 1.45, 1.45],
                              [1.35, 1.60, 1.85, 2.75, 3, 3.25, 3.50, 3.75]]
        i = 0
        for input_box in self.input_boxes:
            input_box.respond_to_resolution(self.button_cont_x * position_fractions[0][i],
                                            self.button_cont_y * position_fractions[1][i])
            i += 1
