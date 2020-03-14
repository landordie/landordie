"""
Constants here
"""
import pygame as pg
from pymunk import Vec2d

pg.font.init()

DEFAULT_FONT = "PressStart2P.ttf"  # To instantiate a font use pygame.font.Font(DEFAULT_FONT, font size)
# ------------------------COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GREY = (192, 192, 192)
DARK_GREY = (128, 128, 128)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHT_PURPLE = (140, 123, 192)
BLACK_HIGHLIGHT = (0, 0, 0, 150)
BLACK_HIGHLIGHT2 = (0, 0, 0, 200)
BLACK_INVISIBLE = (0, 0, 0, 0)
WHITE_HIGHLIGHT = (255, 255, 255, 150)

# ------------------------BUTTON SIZE
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 60

# ------------------------SCENE SIZES
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 800

# ------------------------SOUNDS
HOVER_SOUND = "blipshort1.wav"

# ------------------------PYMUNK
FPS = 60
EARTH_GRAVITY = 0, -700
TERRAIN_THICKNESS = 35
TERRAIN_FRICTION = 1.
SEGMENT_LENGTH = 90

ANTI_SPACECRAFT_WHEEL_SIZE = 15
ANTI_SPACECRAFT_MOVE_FORCE = 35
ANTI_SPACECRAFT_CHASSIS = (50, 15)
ANTI_SPACECRAFT_CANNON = (50, 5)
DEFAULT_FORCE = (0, 0)
DEFAULT_MOMENT = 1
DEFAULT_MASS = 1
DEFAULT_FRICTION = .5
DEFAULT_CONTROLS = ['A', 'W', 'D', 'Left', 'Up', 'Right', 'Down', 'Space']

CONTROL_DICT = {
        'Q': pg.K_q,
        'W': pg.K_w,
        'E': pg.K_e,
        'R': pg.K_r,
        'T': pg.K_t,
        'Y': pg.K_y,
        'U': pg.K_u,
        'I': pg.K_i,
        'O': pg.K_o,
        'P': pg.K_p,
        '[': pg.K_LEFTBRACKET,
        ']': pg.K_RIGHTBRACKET,
        'A': pg.K_a,
        'S': pg.K_s,
        'D': pg.K_d,
        'F': pg.K_f,
        'G': pg.K_g,
        'H': pg.K_h,
        'J': pg.K_j,
        'K': pg.K_k,
        'L': pg.K_l,
        ';': pg.K_SEMICOLON,
        "'": pg.K_QUOTE,
        '#': pg.K_HASH,
        'BSlash': pg.K_BACKSLASH,
        'Z': pg.K_z,
        'X': pg.K_x,
        'C': pg.K_c,
        'V': pg.K_v,
        'B': pg.K_b,
        'N': pg.K_n,
        'M': pg.K_m,
        ',': pg.K_COMMA,
        '.': pg.K_PERIOD,
        'Slash': pg.K_SLASH,
        '1': pg.K_1,
        '2': pg.K_2,
        '3': pg.K_3,
        '4': pg.K_4,
        '5': pg.K_5,
        '6': pg.K_6,
        '7': pg.K_7,
        '8': pg.K_8,
        '9': pg.K_9,
        '0': pg.K_0,
        '-': pg.K_MINUS,
        '=': pg.K_EQUALS,
        'Asterisk': pg.K_ASTERISK,
        '+': pg.K_PLUS,
        '`': pg.K_BACKQUOTE,
        'Up': pg.K_UP,
        'Down': pg.K_DOWN,
        'Space': pg.K_SPACE,
        'Left': pg.K_LEFT,
        'Right': pg.K_RIGHT,
        'LAlt': pg.K_LALT,
        'RAlt': pg.K_RALT,
        'LCtrl': pg.K_LCTRL,
        'RCtrl': pg.K_RCTRL,
        'LShift': pg.K_LSHIFT,
        'RShift': pg.K_RSHIFT,
        'Tab': pg.K_TAB,
        'Enter': pg.K_RETURN
}


def flipy(p, h):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1] + h)
