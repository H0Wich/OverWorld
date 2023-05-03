import os
from tkinter import Place


TITLE = "OverWorld | By HoWich"
WIDTH = 480
HEIGHT = 500
FPS = 60
GRID = 20
GRID_STEP = 24

FONT_NAME = 'fonts.ttf'

PLAYER_ACCELERATION = 0.6
PLAYER_FRICTION = -0.10
PLAYER_GRAVITY_CONSTANT = 0.7
PLAYER_JUMP = 18

PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64

COIN_SPAWN_CHANCE = 10
SCORE_PER_COIN = 10
MOB_SPAWN_FREQUENCY = 5000
HARDNESS = 0
MAX_HARDNESS = 4

PLAYER_LAYER = 2
PLATFORM_LAYER = 3
COIN_LAYER = 3
BAT_LAYER = 5
WARNING_SIGN_LAYER = 4

PLATFORM_COUNT = 8
PLATFORM_HEIGHT = 24
PLATFORM_MAX_SECTIONS = 5
PLATFORM_START_LIST = [(8 * GRID_STEP, HEIGHT - 2 * GRID_STEP, 3),
                       (2 * GRID_STEP, HEIGHT - 5 * GRID_STEP, 4),
                       (5 * GRID_STEP, HEIGHT - 7 * GRID_STEP, 3),
                       (8 * GRID_STEP, HEIGHT - 9 * GRID_STEP, 5),
                       (3 * GRID_STEP, HEIGHT - 12 * GRID_STEP, 3),
                       (16 * GRID_STEP, HEIGHT - 14 * GRID_STEP, 3),
                       (9 * GRID_STEP, HEIGHT - 16 * GRID_STEP, 5),
                       (12 * GRID_STEP, HEIGHT - 18 * GRID_STEP, 4)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
