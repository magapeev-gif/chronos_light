"""Точка входа: игровой цикл и состояния игры."""
import sys
import pygame
from constants import *
from level import Level
from player import Player
from light import compute_light
import ui


def new_game():
    """Создаёт уровень и игрока для новой партии."""
    return Level(), Player(*PLAYER_START)


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    big_font = pygame.font.Font(None, 64)

    state = STATE_MENU
    level = player = None
    lit_cells, polygon = set(), []
    time_left = TIME_LIMIT
    debug = False
    dt = 0.0

    while True:
        # 1. СОБЫТИЯ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    debug = not debug
                match state:
                    case "MENU":
                        if event.key == pygame.K_RETURN:
                            level, player = new_game()
                            time_left = TIME_LIMIT
                            state = STATE_PLAY
                    case "PLAY":
                        if event.key == pygame.K_ESCAPE:
                            state = STATE_MENU
                    case "WIN" | "LOSE":
                        if event.key == pygame.K_RETURN:
                            state = STATE_MENU

        # 2. ОБНОВЛЕНИЕ
        if state == STATE_PLAY:
            time_left -= dt
            player.update(pygame.key.get_pressed(), pygame.mouse.get_pos(), level, dt)
            # Свет считаем ДО обновления стен: сдвигаем только то, что не освещено
            lit_cells, polygon = compute_light(level, *player.center, player.alpha)
            level.update(dt, lit_cells, player.rect)
            ex, ey = EXIT_CELL
            exit_rect = pygame.Rect(ex * TILE_SIZE, ey * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if player.rect.colliderect(exit_rect):
                state = STATE_WIN
            elif time_left <= 0:
                state = STATE_LOSE

        # 3. ОТРИСОВКА
        if state == STATE_MENU:
            ui.draw_menu(screen, font, big_font)
        else:
            screen.fill(COLORS["bg"])
            # Полупрозрачный конус света
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            if len(polygon) > 2:
                pygame.draw.polygon(overlay, COLORS["light"], polygon)
            screen.blit(overlay, (0, 0))
            level.draw(screen, lit_cells, debug)
            player.draw(screen)
            shadow = level.count_walls() - len(lit_cells)
            ui.draw_hud(screen, font, max(time_left, 0), shadow)
            if state in (STATE_WIN, STATE_LOSE):
                ui.draw_end(screen, font, big_font, state == STATE_WIN, time_left)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000.0         # секунды, прошедшие за кадр


if __name__ == "__main__":
    main()