#------------------------------------------#

# Code for scene architecture taken from:
# https: // nerdparadise.com / programming / pygame / part7

#------------------------------------------#

from classes.Scenes import *


def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display
    screen.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
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
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    myScene = TitleScene()
    screenWidth = 800
    screenHeight = 600
    run_game(screenWidth, screenHeight, 60, TitleScene())
