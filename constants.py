"""
Constants here
"""
import pygame as pg
from pymunk import Vec2d

pg.font.init()

# ------------------------FONTS
FONT_BIG = pg.font.Font("PressStart2P.ttf", 18)
FONT_MEDIUM_PLUS = pg.font.Font("PressStart2P.ttf", 17)
FONT_MEDIUM = pg.font.Font("PressStart2P.ttf", 16)
FONT_SMALL_PLUS = pg.font.Font("PressStart2P.ttf", 15)
FONT_SMALL = pg.font.Font("PressStart2P.ttf", 14)
FONT_HEADER = pg.font.Font("PressStart2P.ttf", 50)
FONT_WARNING = pg.font.Font("PressStart2P.ttf", 27)

# ------------------------COLORS
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)
LIGHT_BLUE = (0, 100, 255, 255)
YELLOW = (255, 255, 0, 255)
LIGHT_GREY = (192, 192, 192, 255)
DARK_GREY = (128, 128, 128, 255)
MAGENTA = (255, 0, 255, 255)
CYAN = (0, 255, 255, 255)
LIGHT_PURPLE = (140, 123, 192, 255)
BRIGHT_PURPLE = (163, 52, 207, 255)
BLACK_HIGHLIGHT = (0, 0, 0, 150)
BLACK_HIGHLIGHT2 = (0, 0, 0, 200)
BLACK_HIGHLIGHT3 = (0, 0, 0, 240)
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

ANTI_SPACECRAFT_WHEEL_SIZE = 13
ANTI_SPACECRAFT_MOVE_FORCE = 35
ANTI_SPACECRAFT_WHEEL_MASS = 0.85
ANTI_SPACECRAFT_CHASSIS_MASS = 0.2
ANTI_SPACECRAFT_CANNON_MASS = 0.03
ANTI_SPACECRAFT_CHASSIS = (50, 15)
ANTI_SPACECRAFT_CANNON = (50, 5)
DEFAULT_FORCE = (0, 0)
DEFAULT_MOMENT = 1
DEFAULT_MASS = 1
DEFAULT_FRICTION = .5
DEFAULT_CONTROLS = ['A', 'W', 'D', 'Left', 'Up', 'Right', 'Down', 'Space']

# Constant used in calculating mid-air velocity of missiles every frame (air resistance effect)
MISSILE_DRAG_CONSTANT = 0.0002

CONTROLS_DICT = {
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
