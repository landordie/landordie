"""
'scene_base.py' module.
Contains SceneBase abstract superclass implementation.
"""
from .constants import DEFAULT_WIDTH, DEFAULT_HEIGHT


class SceneBase:
    """
    Superclass of all the other scene classes in src - MenuScene, SplashScene, AccountsScene
    GameScene and ResultScene. It defines 7 abstract methods - process_input(), update(), render(),
    switch_to_scene(), terminate(), adjust_screen(). Each method is inherited by the
    above src and overwritten with the functionality required by the particular class.
    """
    screen_width = DEFAULT_WIDTH
    screen_height = DEFAULT_HEIGHT

    def __init__(self):
        """Virtually private constructor which initializes the SceneBase superclass."""
        self.next = self
        self.background = None  # The background image
        self.x = 0  # Attribute to simulate the x-axis position of the background image
        # (parallax effect in some scenes)

    def process_input(self, events, pressed_keys):
        """
        Process all the events that occur in the environment (game window). Every frame
        a list of all the filtered events (the ones we care about - button presses,
        mouse movement, etc.) are passed to this method. It then executes the functionality
        specified for each event of interest.
        :param events: program scene event
        :param pressed_keys: pressed keys input
        """
        print("(!) Override in child class (!)")

    def update(self):
        """Update any variables (attributes) within the frames."""
        print("(!) Override in child class (!)")

    def render(self, screen):
        """
        Render the scene by displaying all objects on the screen (backgrounds, sprites, Pymunk
        shapes, terrain, etc.). It reflects any changes on variables as it is executed every frame.
        :param screen: scene screen (window)
        """
        print("(!) Override in child class (!)")

    def switch_to_scene(self, next_scene):
        """
        Change the focus of the main program from one scene to another. For example, when the Options
        button is clicked in the Menu scene the switch_to_scene() method is setting the '.next' attribute
        of the current scene to an OptionsScene instance. This changes the 'current_scene' variable in the
        main module to the OptionsScene singleton instance. Now the program is operating with the new scene
        methods instead.
        :param next_scene: scene instance to switch to
        """
        self.next = next_scene

    def terminate(self):
        """
        Set the current scene '.next' variable to None. That is how clicking on the 'X' (exit) button
        of the window stops the game. (Essentially calls the switch_to_scene() method with 'next_scene'
        parameter set to None)
        """
        self.switch_to_scene(None)

    def adjust_screen(self, screen):
        """
        Update screen changes (resolution) and return the new surface
        :param screen:
        :return: surface of the screen
        """
        screen.set_mode((self.screen_width, self.screen_height))  # Set the screen size
        return screen.get_surface()  # Get the surface of the screen

    def parallax_effect(self, display):
        """
        Introduce a background parallax effect. (MenuScene, OptionsScene, AccountsScene)
        :param display: current scene screen surface
        """
        img_width = self.background.get_rect().width
        rel_x = self.x % img_width  # The relative x-axis position of the image used for the parallax effect
        # Displaying the image based on the relative x-axis position and the image width
        display.blit(self.background, (rel_x - img_width, 0))

        # When the right end of the image reaches the right side of the screen
        # a new image starts displaying so we do not have any black spaces
        if rel_x < self.screen_width:
            display.blit(self.background, (rel_x, 0))
        self.x -= 1  # This decrement is what makes the image "move"

