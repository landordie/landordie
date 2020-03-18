from constants import *


class InputBox:
    # class variable with all input box texts
    boxes = DEFAULT_CONTROLS
    no = 0

    def __init__(self, x, y, text='', w=100, h=35):
        self.rect = pg.Rect(x, y, w, h)
        self.color = BRIGHT_PURPLE
        self.text = text
        self.txt_surface = pg.font.Font(DEFAULT_FONT, 18).render(text, True, WHITE)
        self.id_num = InputBox.no

        InputBox.no += 1
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.key == pg.K_UP:
                        self.text = 'Up'
                    elif event.key == pg.K_DOWN:
                        self.text = 'Down'
                    elif event.key == pg.K_LEFT:
                        self.text = 'Left'
                    elif event.key == pg.K_RIGHT:
                        self.text = 'Right'
                    elif event.key == pg.K_LSHIFT:
                        self.text = 'LShift'
                    elif event.key == pg.K_RSHIFT:
                        self.text = 'RShift'
                    elif event.key == pg.K_LCTRL:
                        self.text = 'LCtrl'
                    elif event.key == pg.K_RCTRL:
                        self.text = 'RCtrl'
                    elif event.key == pg.K_SPACE:
                        self.text = 'Space'
                    elif event.key == pg.K_LALT:
                        self.text = 'LAlt'
                    elif event.key == pg.K_RALT:
                        self.text = 'RAlt'
                    elif event.key == pg.K_RETURN:
                        self.text = 'Enter'
                    elif event.key == pg.K_TAB:
                        self.text = 'Tab'
                    elif event.key == pg.K_BACKSLASH:
                        self.text = 'BSlash'
                    elif event.key == pg.K_SLASH:
                        self.text = 'Slash'
                    elif event.key == pg.K_ASTERISK:
                        self.text = 'Asterisk'
                    else:
                        self.text = event.unicode.upper()

                    # update boxes list
                    InputBox.boxes[self.id_num] = self.text
                    self.active = False
                # Re-render the text.
                self.txt_surface = pg.font.Font(DEFAULT_FONT, 18).render(self.text, True, WHITE)
        # Change the current color of the input box.
        self.color = CYAN if self.active else BRIGHT_PURPLE

    def update(self):
        # Resize the box if the text is too long.
        width = max(50, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 3)

    def respond_to_resolution(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
