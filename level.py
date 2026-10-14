"""Лабиринт: матрица клеток и динамический сдвиг невидимых стен."""
import random
import pygame
from constants import *

# 1 - стена, 0 - пол. Размер 20x15. Внешняя рамка неподвижна.
LEVEL_MAP = [
    "11111111111111111111",
    "10000000010000000001",
    "10111110010111011101",
    "10100000000100000001",
    "10101111110101111101",
    "10000000000000000001",
    "11110111111011110111",
    "10000100000000100001",
    "10111101111110101101",
    "10000000000000100001",
    "10111111011110111101",
    "10000000010000000001",
    "10111101010111111101",
    "10000001000000000001",
    "11111111111111111111",
]

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class Level:
    def __init__(self):
        # Проверяем, что карта имеет правильный размер
        if len(LEVEL_MAP) != GRID_ROWS or any(len(r) != GRID_COLUMNS for r in LEVEL_MAP):
            raise ValueError("LEVEL_MAP должна быть 20x15")
        # Матрица чисел: grid[y][x]
        self.grid = [[int(ch) for ch in row] for row in LEVEL_MAP]
        # Счётчики теней: {(gx, gy): секунд в темноте}
        self.timers = {}

    # ---------- запросы к матрице ----------
    def is_wall(self, gx, gy):
        if 0 <= gx < GRID_COLUMNS and 0 <= gy < GRID_ROWS:
            return self.grid[gy][gx] == TILE_WALL
        return True                       # за границей карты - стена

    def is_movable_zone(self, gx, gy):
        """Внешняя рамка двигаться не может."""
        return 1 <= gx <= GRID_COLUMNS - 2 and 1 <= gy <= GRID_ROWS - 2

    def blocked(self, rect):
        """True, если прямоугольник игрока задевает стену (проверка 4 углов)."""
        corners = [(rect.left, rect.top), (rect.right - 1, rect.top),
                   (rect.left, rect.bottom - 1), (rect.right - 1, rect.bottom - 1)]
        return any(self.is_wall(x // TILE_SIZE, y // TILE_SIZE) for x, y in corners)

    def count_walls(self):
        return sum(row.count(TILE_WALL) for row in self.grid)

    # ---------- трансформация лабиринта ----------
    def _try_shift(self, gx, gy, player_rect):
        """Сдвигает стену на 1 клетку в случайную свободную сторону."""
        dirs = DIRECTIONS[:]
        random.shuffle(dirs)              # случайный порядок проверки сторон
        for dx, dy in dirs:
            tx, ty = gx + dx, gy + dy
            if not self.is_movable_zone(tx, ty):
                continue                  # не выходим на рамку
            if self.grid[ty][tx] != TILE_FLOOR:
                continue                  # клетка занята
            if (tx, ty) == EXIT_CELL:
                continue                  # выход не закрываем
            cell = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell.colliderect(player_rect):
                continue                  # не замуровываем игрока "на месте"
            self.grid[gy][gx] = TILE_FLOOR
            self.grid[ty][tx] = TILE_WALL
            return (tx, ty)
        return None                       # свободной стороны нет

    def update(self, dt, lit_cells, player_rect):
        """Обновляет счётчики теней и двигает стены, просидевшие в тени 3 с."""
        # Актуальный набор подвижных стен
        walls = [(x, y) for y in range(1, GRID_ROWS - 1)
                 for x in range(1, GRID_COLUMNS - 1) if self.grid[y][x] == TILE_WALL]
        # Убираем счётчики стен, которых уже нет на этом месте
        self.timers = {c: t for c, t in self.timers.items() if c in walls}

        for cell in walls:
            if cell in lit_cells:
                self.timers[cell] = 0.0                       # на стену падает свет
                continue
            self.timers[cell] = self.timers.get(cell, 0.0) + dt   # стена в тени
            if self.timers[cell] >= WALL_SHIFT_INTERVAL:
                new_cell = self._try_shift(cell[0], cell[1], player_rect)
                self.timers.pop(cell, None)
                if new_cell:
                    self.timers[new_cell] = 0.0               # у новой клетки счёт с нуля

    # ---------- отрисовка ----------
    def draw(self, surface, lit_cells, debug=False):
        for (gx, gy) in lit_cells:                            # освещённые стены - белые
            r = pygame.Rect(gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, COLORS["wall_lit"], r)
        if debug:                                             # F1: показать тёмные стены
            for y, row in enumerate(self.grid):
                for x, tile in enumerate(row):
                    if tile == TILE_WALL and (x, y) not in lit_cells:
                        r = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(surface, COLORS["wall_debug"], r)
        ex, ey = EXIT_CELL                                    # выход виден всегда
        pygame.draw.rect(surface, COLORS["exit"],
                         (ex * TILE_SIZE + 6, ey * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12))