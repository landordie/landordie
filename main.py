"""
'main.py' module.
Runs the game loop.
"""
# ------------------------------------------#

# Code for scene architecture taken from:
# https: // nerdparadise.com / programming / pygame / part7

# ------------------------------------------#

import pygame as pg
from src.menu_scene import MenuScene


class Game:
    """Game class implementation."""

    def __init__(self):
        """Virtually private constructor which initializes the Game class instance."""
        self.menu = MenuScene()  # Initialize the Menu scene for our starting scene
        self.run_game(60, self.menu)  # Run the game on 60 fps

    @staticmethod
    def run_game(fps, starting_scene):
        """
        Run the main loop of the program.
        :param fps: frames per second
        :param starting_scene: the starting scene of the game
        """
        # Initialize Pygame objects
        pg.init()
        screen = pg.display
        clock = pg.time.Clock()
        pg.display.set_caption('LAND OR DIE')

        # Set the active scene to the starting scene
        active_scene = starting_scene

        # If there is an active scene start program loop
        while active_scene is not None:
            # Variable to check for keys being pressed or held down
            pressed_keys = pg.key.get_pressed()

            filtered_events = []  # Event filtering
            for event in pg.event.get():
                quit_attempt = False
                if event.type == pg.QUIT:  # If the player presses the 'X' button
                    quit_attempt = True
                # If the player presses the 'Esc' button
                # or tries the 'Alt+F4' key combination
                elif event.type == pg.KEYDOWN:
                    alt_pressed = pressed_keys[pg.K_LALT] or \
                                  pressed_keys[pg.K_RALT]
                    if event.key == pg.K_ESCAPE:
                        quit_attempt = True
                    elif event.key == pg.K_F4 and alt_pressed:
                        quit_attempt = True
                if quit_attempt:  # On player trying to quit
                    active_scene.terminate()  # Terminate the program loop
                else:
                    filtered_events.append(event)  # Add the events into the filtered list

            # Pass the list of events and pressed keys for processing by the current scene
            active_scene.process_input(filtered_events, pressed_keys)

            # Render current scene's objects to the screen
            active_scene.render(screen)

            # Switch the scene after exiting the current scene loop
            prev_scene = active_scene
            active_scene = active_scene.next
            prev_scene.next = prev_scene

            # Update the display
            pg.display.flip()
            clock.tick(fps)


# Initiate the program loop with the first scene
myGame = Game()
