"""Все настройки игры в одном месте."""

# --- Окно ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
TITLE = "Chronos Light - ЛР 1"

# --- Сетка ---
TILE_SIZE = 40
GRID_COLUMNS = WINDOW_WIDTH // TILE_SIZE    # 20
GRID_ROWS = WINDOW_HEIGHT // TILE_SIZE      # 15

# --- Тайлы ---
TILE_FLOOR = 0
TILE_WALL = 1

# --- Игрок ---
PLAYER_SIZE = 22
PLAYER_SPEED = 150          # пикселей в секунду
PLAYER_START = (1, 1)       # клетка старта (gx, gy)
EXIT_CELL = (18, 13)        # клетка выхода

# --- Фонарик ---
LIGHT_HALF_ANGLE = 30       # половина раствора конуса, градусы
LIGHT_RAY_COUNT = 61        # количество лучей (шаг 1 градус)
LIGHT_RANGE = 240           # дальность света, пиксели
LIGHT_STEP = 2              # шаг движения луча, пиксели

# --- Стены ---
WALL_SHIFT_INTERVAL = 3.0   # секунд в тени до сдвига

# --- Игра ---
TIME_LIMIT = 90             # секунд на прохождение

# --- Цвета ---
COLORS = {
    "bg": (0, 0, 0),
    "wall_lit": (255, 255, 255),
    "wall_debug": (60, 60, 60),
    "light": (255, 240, 150, 55),   # RGBA, полупрозрачный конус
    "player": (40, 140, 255),
    "exit": (30, 160, 70),
    "text": (255, 255, 255),
}

# --- Состояния ---
STATE_MENU = "MENU"
STATE_PLAY = "PLAY"
STATE_WIN = "WIN"
STATE_LOSE = "LOSE"