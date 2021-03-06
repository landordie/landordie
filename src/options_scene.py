"""
'options_scene.py' module.
Used in instantiation of the Options scene (window).
"""
from .constants import *
from .menu_scene import MenuScene
from .input_box import InputBox
from .scene_base import SceneBase
from .button import Button
from .controls import Controls
from .helper import draw_text


class OptionsScene(SceneBase):
    """OptionsScene singleton subclass implementation."""
    __instance = None

    @staticmethod
    def get_instance():
        """
        Static access method. Ensures the singularity of a class instance.
        :return: OptionsScene class instance
        """
        if OptionsScene.__instance is None:
            OptionsScene()
        return OptionsScene.__instance

    def __init__(self):
        """Virtually private constructor which initializes the Options scene."""
        # Call the super class (SceneBase) initialization method. This
        # statement ensures that this class inherits its behaviour from its Superclass.
        # Abstract methods of all scenes (process_input(), update(), render(), etc.), screen
        # resolutions, text fonts, general text drawing methods and so on.
        super().__init__()

        # Check if there are any instances of the class already created
        if OptionsScene.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            OptionsScene.__instance = self

        self.background = pg.image.load("assets/frames/BG.png")  # Initialize the background

        # Create button allowing the user to return to main menu
        self.menu_button = Button((self.screen_width * 0.25, self.screen_height * 0.8, BUTTON_WIDTH, BUTTON_HEIGHT),
                                  YELLOW, 'Main Menu')

        # Container for resolution buttons
        self.res_cont_w, self.res_cont_h = self.screen_width / 5, self.screen_height / 3
        self.res_cont_x, self.res_cont_y = (self.screen_width / 8.3), (self.screen_height / 3)
        self.res_cont = pg.Surface((self.res_cont_w, self.res_cont_h)).convert_alpha()
        self.res_cont.fill(BLACK_HIGHLIGHT2)

        # Buttons to change resolution
        self._res1 = Button((self.res_cont_w / 1.475, self.res_cont_h / 0.91, BUTTON_WIDTH, BUTTON_HEIGHT),
                            GREEN, "1280x800")
        self._res2 = Button((self.res_cont_w / 1.475, self.res_cont_h / 0.64, BUTTON_WIDTH, BUTTON_HEIGHT),
                            GREEN, "1440x900")

        # Container for controls boxes
        self.controls_cont_w, self.controls_cont_h = self.screen_width / 2.8, self.screen_height / 1.7
        self.controls_cont_x, self.controls_cont_y = (self.screen_width / 1.9), (self.screen_height / 5.4)
        self.controls_cont = pg.Surface((self.controls_cont_w, self.controls_cont_h)).convert_alpha()
        self.controls_cont.fill(BLACK_HIGHLIGHT2)

        # Input boxes to change controls (and a list allowing iteration over the input boxes)
        # ('sc' - spacecraft, 'a_sc' - anti-spacecraft)
        self.sc_left = InputBox(self.controls_cont_x * 1.5, self.controls_cont_y * 1.35, 'A')
        self.sc_thrust = InputBox(self.controls_cont_x * 1.5, self.controls_cont_y * 1.60, 'W')
        self.sc_right = InputBox(self.controls_cont_x * 1.5, self.controls_cont_y * 1.85, 'D')

        self.a_sc_left = InputBox(self.controls_cont_x * 1.45, self.controls_cont_y * 2.75, 'Left')
        self.cannon_right = InputBox(self.controls_cont_x * 1.45, self.controls_cont_y * 3, 'Up')
        self.a_sc_right = InputBox(self.controls_cont_x * 1.45, self.controls_cont_y * 3.25, 'Right')
        self.cannon_left = InputBox(self.controls_cont_x * 1.45, self.controls_cont_y * 3.5, 'Down')
        self.cannon_shoot = InputBox(self.controls_cont_x * 1.45, self.controls_cont_y * 3.75, 'Space')
        self.input_boxes = [self.sc_left, self.sc_thrust, self.sc_right, self.a_sc_left, self.cannon_right,
                            self.a_sc_right, self.cannon_left, self.cannon_shoot]

    def process_input(self, events, pressed_keys):
        for event in events:
            for input_box in self.input_boxes:  # Handle input box events
                input_box.handle_event(event)
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:  # Quit on 'Esc' button press
                self.terminate()
            # Handle change of resolution. (update resolutions (globally) in the superclass
            # so that it is reflected in every scene)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self._res1.on_click(event):
                    _res = self._res1.text_string.split("x")
                    SceneBase.screen_width, SceneBase.screen_height = int(_res[0]), int(_res[1])
                    self.update()
                elif self._res2.on_click(event):
                    _res = self._res2.text_string.split("x")
                    SceneBase.screen_width, SceneBase.screen_height = int(_res[0]), int(_res[1])
                    self.update()
                elif self.menu_button.on_click(event):  # Switch back to the Menu scene on 'Main Menu' button click
                    input_box_texts = [box.text for box in self.input_boxes]  # Get the (new) controls
                    Controls.update(input_box_texts)  # Update them (globally) in the controls class
                    menu = MenuScene.get_instance()
                    menu.update()
                    self.switch_to_scene(menu)

    def update(self):
        """Reposition all buttons/containers when changing resolutions"""
        # The button that returns to Main Menu
        self.menu_button.rect.x, self.menu_button.rect.y = self.screen_width * 0.25, self.screen_height * 0.8

        # The resolution buttons container
        # prev1, prev2 = self.res_cont_w, self.res_cont_h
        self.res_cont_w, self.res_cont_h = self.screen_width / 5, self.screen_height / 3
        self.res_cont_x, self.res_cont_y = (self.screen_width / 8.3), (self.screen_height / 3)
        self.res_cont = pg.Surface((self.res_cont_w, self.res_cont_h)).convert_alpha()

        # The two buttons for resolutions
        self._res1.rect.x, self._res1.rect.y = self.res_cont_w / 1.475, self.res_cont_h / .91
        self._res2.rect.x, self._res2.rect.y = self.res_cont_w / 1.475, self.res_cont_h / .64

        self.controls_cont_w, self.controls_cont_h = self.screen_width / 2.8, self.screen_height / 1.7
        self.controls_cont_x, self.controls_cont_y = (self.screen_width / 1.9), (self.screen_height / 5.4)
        self.controls_cont = pg.Surface((self.controls_cont_w, self.controls_cont_h)).convert_alpha()

        # Make adjustments to the input box positions by iterating over the list
        position_fractions = [[1.5, 1.5, 1.5, 1.45, 1.45, 1.45, 1.45, 1.45],
                              [1.35, 1.60, 1.85, 2.75, 3, 3.25, 3.50, 3.75]]
        i = 0
        for input_box in self.input_boxes:
            input_box.respond_to_resolution(self.controls_cont_x * position_fractions[0][i],
                                            self.controls_cont_y * position_fractions[1][i])
            i += 1

    def render(self, screen):
        display = self.adjust_screen(screen)  # Surface
        self.parallax_effect(display)  # Initialize the parallax effect

        # Drawing the containers and displaying info text
        # (!) Containers are displayed relative to the screen size;
        # (!) Buttons are displayed relative to the containers position
        display.blit(self.res_cont, (self.res_cont_x, self.res_cont_y, self.res_cont_w, self.res_cont_h))
        draw_text(display, "Resolution", (self.res_cont_x + self.res_cont_w / 2, self.res_cont_y / 1.1),
                  FONT_MEDIUM, WHITE)

        display.blit(self.controls_cont,
                     (self.controls_cont_x, self.controls_cont_y, self.controls_cont_w, self.controls_cont_h))
        draw_text(display, "Controls", (self.controls_cont_x + self.controls_cont_w // 2, self.controls_cont_y // 1.1),
                  FONT_MEDIUM, WHITE)
        draw_text(display, "Spacecraft", (self.controls_cont_x + self.controls_cont_w / 2, self.controls_cont_y * 1.2),
                  FONT_MEDIUM, WHITE)
        draw_text(display, "Anti-Spacecraft",
                  (self.controls_cont_x + self.controls_cont_w / 2, self.controls_cont_y * 2.6), FONT_MEDIUM, WHITE)

        draw_text(display, "Thrust", (self.sc_left.rect.x * 0.8, self.sc_thrust.rect.y * 1.08),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Rotate Left", (self.sc_left.rect.x * 0.8, self.sc_left.rect.y * 1.08),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Rotate Right", (self.sc_left.rect.x * 0.8, self.sc_right.rect.y * 1.08),
                  FONT_MEDIUM, LIGHT_GREY)

        draw_text(display, "Move Left", (self.a_sc_left.rect.x * 0.85, self.a_sc_left.rect.y * 1.04),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Cannon Right", (self.cannon_right.rect.x * 0.85, self.cannon_right.rect.y * 1.04),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Move Right", (self.a_sc_right.rect.x * 0.85, self.a_sc_right.rect.y * 1.04),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Cannon Left", (self.cannon_left.rect.x * 0.85, self.cannon_left.rect.y * 1.04),
                  FONT_MEDIUM, LIGHT_GREY)
        draw_text(display, "Shoot", (self.cannon_shoot.rect.x * 0.85, self.cannon_shoot.rect.y * 1.04),
                  FONT_MEDIUM, LIGHT_GREY)

        self.menu_button.update(display)
        self._res1.update(display)
        self._res2.update(display)

        # Display and update input box fields
        for input_box in self.input_boxes:
            input_box.draw(display)
            input_box.update()
