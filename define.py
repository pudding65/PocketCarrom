import os
import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOARD_SIZE = (800, 800)


BOARD_POSITION = ((WINDOW_WIDTH - BOARD_SIZE[0]) // 2, (WINDOW_HEIGHT - BOARD_SIZE[1]) // 2)
START_POSITION = (WINDOW_WIDTH / 2 - 140, WINDOW_HEIGHT / 3 - 60)
OPTIONS_POSITION = (WINDOW_WIDTH / 2 - 140, WINDOW_HEIGHT / 3 + 80)
EXIT_POSITION = (WINDOW_WIDTH / 2 - 140, WINDOW_HEIGHT / 3 + 220)
VOLUME_POSITION = (WINDOW_WIDTH / 2 - 140, WINDOW_HEIGHT / 3 - 60)
CREDITS_POSITION = (WINDOW_WIDTH / 2 - 140, WINDOW_HEIGHT / 3 + 80)

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_LIGHT_BROWN = (255, 198, 151)
COLOR_DARK_BROWN = (178, 138, 105)
COLOR_BACKGROUND = (253, 175, 123)


PATH_DIRECTORY = os.path.dirname(__file__)
PATH_IMAGE = os.path.join(PATH_DIRECTORY, "assets/game/")
PATH_MENU = os.path.join(PATH_DIRECTORY, "assets/menu/")

# Khởi tạo force và các hằng số liên quan
MAXFORCE = 100
INCREASE_RATE = 80  # Tốc độ tăng lực mỗi giây
DECREASE_RATE = 80  # Tốc độ giảm lực mỗi giây
POCKET_DIA = 48  # Đường kính lỗ
#tạo cạnh bàn carrom
CUSHION = [
    [(200,0), (260,38), (1000,0), (940,38)],
    [(200,0), (239,60), (200,800), (239,740)],
    [(1000,0), (961,60), (1000,800), (961,740)],
    [(200,800), (260,762), (1000,800), (940,762)]
]
# tạo lỗ
POCKETS = [
    (265, 61),
    (941, 58),
    (942, 736),
    (266,729)
]

#game variables
DIA = 38
#TAKING_SHOT = True