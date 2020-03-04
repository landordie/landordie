# ------------------------------------------#

# Code for scene architecture taken from:
# https: // nerdparadise.com / programming / pygame / part7

# ------------------------------------------#

from classes.scene_base import *
from classes import *

class Game:
    def __init__(self):
        self.menu = MenuScene()
        self.game = GameScene()
        self.options = OptionsScene()
        self.run_game(self.menu.width, self.menu.height, 60, self.menu)

    def run_game(self, width, height, fps, starting_scene):
        """Function to run the program"""
        # Initialize pygame objects
        pygame.init()
        screen = pygame.display
        screen.set_mode((width, height))
        clock = pygame.time.Clock()

        # Set the active scene
        active_scene = starting_scene

        # If there is an active scene start program loop
        while active_scene is not None:
            pressed_keys = pygame.key.get_pressed()

            # Event filtering
            filtered_events = []
            for event in pygame.event.get():
                quit_attempt = False
                # If a quit is attempted
                if event.type == pygame.QUIT:
                    quit_attempt = True
                elif event.type == pygame.KEYDOWN:
                    alt_pressed = pressed_keys[pygame.K_LALT] or \
                                  pressed_keys[pygame.K_RALT]
                    if event.key == pygame.K_ESCAPE:
                        quit_attempt = True
                    elif event.key == pygame.K_F4 and alt_pressed:
                        quit_attempt = True

                if quit_attempt:
                    active_scene.Terminate()
                else:
                    # If not quitting add events into list
                    filtered_events.append(event)

            # Pass the list of events and pressed keys for processing by the current scene
            active_scene.ProcessInput(filtered_events, pressed_keys)
            active_scene.Update()
            # Render current scene's objects to the screen
            active_scene.Render(screen)

            # Switch the scene after exiting the current scene loop
            prev_scene = active_scene
            active_scene = active_scene.next
            prev_scene.next = prev_scene

            # Update the display
            pygame.display.flip()
            clock.tick(fps)


# Initiate the program loop with the first scene
myGame = Game()
