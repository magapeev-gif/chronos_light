"""Интерфейс: меню, HUD, экраны победы и поражения."""
import pygame
from constants import *


def _center(surface, font, text, y):
    img = font.render(text, True, COLORS["text"])
    surface.blit(img, img.get_rect(center=(WINDOW_WIDTH // 2, y)))


def draw_menu(surface, font, big_font):
    surface.fill(COLORS["bg"])
    _center(surface, big_font, "CHRONOS LIGHT", 190)
    _center(surface, font, "Лабиринт тёмен. Стены двигаются, пока на них не падает свет.", 270)
    _center(surface, font, "WASD - движение, мышь - направление фонарика", 310)
    _center(surface, font, "Дойдите до зелёного выхода за 90 секунд", 350)
    _center(surface, font, "F1 - показать тёмные стены (отладка)   ENTER - старт", 420)


def draw_hud(surface, font, time_left, shadow_count):
    text = f"Время: {int(time_left)}с    Стен в тени: {shadow_count}"
    surface.blit(font.render(text, True, COLORS["text"]), (10, 8))


def draw_end(surface, font, big_font, win, time_left):
    # Полупрозрачное затемнение поверх игры
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    _center(surface, big_font, "ВЫ ВЫБРАЛИСЬ!" if win else "ВРЕМЯ ВЫШЛО", 250)
    if win:
        _center(surface, font, f"Осталось времени: {int(time_left)}с", 310)
    _center(surface, font, "ENTER - в меню", 370)