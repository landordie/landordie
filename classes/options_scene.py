from classes import MenuScene
from classes.input_box import InputBox
from .game_scene import *
from .button import Button


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
        self.input_boxes = []

        self.menu_button = Button(
            (self.screen_width * 0.75 - (BUTTON_WIDTH / 2), self.screen_height * 0.75, BUTTON_WIDTH, BUTTON_HEIGHT), YELLOW,
            'Main Menu')

        self._res2 = Button((self.screen_width * 0.25 - (BUTTON_WIDTH / 2), self.screen_height * 0.25, BUTTON_WIDTH, BUTTON_HEIGHT),
                            GREEN, "1280x720")
        self._res3 = Button((self.screen_width * 0.25 - (BUTTON_WIDTH / 2), self.screen_height * 0.35, BUTTON_WIDTH, BUTTON_HEIGHT),
                            GREEN, "1440x900")

        self.input_box1 = InputBox(self.screen_width / 1.6, self.screen_height / 5, 100, 35, 'A')
        self.input_box2 = InputBox(self.screen_width / 1.37, self.screen_height / 9, 100, 35, 'W')
        self.input_box3 = InputBox(self.screen_width / 1.2, self.screen_height / 5, 100, 35, 'D')

        self.input_box4 = InputBox(self.screen_width / 1.6, self.screen_height / 2, 100, 35, 'Left')
        self.input_box5 = InputBox(self.screen_width / 1.37, self.screen_height / 2.75, 100, 35, 'Up')
        self.input_box6 = InputBox(self.screen_width / 1.2, self.screen_height / 2, 100, 35, 'Right')
        self.input_box7 = InputBox(self.screen_width / 1.37, self.screen_height / 2, 100, 35, 'Down')
        self.input_box8 = InputBox(self.screen_width / 1.1, self.screen_height / 2.5, 100, 35, 'Space')

        self.input_boxes = [self.input_box1, self.input_box2,self.input_box3, self.input_box4, self.input_box5,
                            self.input_box6, self.input_box7, self.input_box8]

    def ProcessInput(self, events, pressed_keys):
        for event in events:

            self.input_box1.handle_event(event)  # input box event handler
            self.input_box2.handle_event(event)
            self.input_box3.handle_event(event)

            self.input_box4.handle_event(event)  # input box event handler
            self.input_box5.handle_event(event)
            self.input_box6.handle_event(event)
            self.input_box7.handle_event(event)  # input box event handler
            self.input_box8.handle_event(event)

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._res3.on_click(event):
                _res = self._res3._text.split("x")
                SceneBase.screen_width, SceneBase.screen_height = int(_res[0]), int(_res[1])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.menu_button.on_click(event):
                # Pass input box texts
                menu = MenuScene.getInstance()
                menu.update_all()
                self.SwitchToScene(menu)

    def Update(self):
        pass

    def Render(self, screen):
        screen.set_mode((self.screen_width, self.screen_height))
        screen.get_surface().fill(BLACK)

        self.menu_button.update(screen.get_surface())
        self._res2.update(screen.get_surface())
        self._res3.update(screen.get_surface())

        self.input_box1.draw(screen.get_surface())
        self.input_box2.draw(screen.get_surface())
        self.input_box3.draw(screen.get_surface())

        self.input_box4.draw(screen.get_surface())
        self.input_box5.draw(screen.get_surface())
        self.input_box6.draw(screen.get_surface())
        self.input_box7.draw(screen.get_surface())
        self.input_box8.draw(screen.get_surface())

        self.input_box1.update()
        self.input_box2.update()
        self.input_box3.update()

        self.input_box4.update()
        self.input_box5.update()
        self.input_box6.update()
        self.input_box7.update()
        self.input_box8.update()
