import pygame

from imports import *


def find_snake_head(gmap: list) -> tuple[int, int]:
    """Return a tuple of snake head coordinates"""
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if gmap[y][x] == 'H':
                return y, x
    return 0, 0


def is_there_apple(gmap: list, pos: pygame.Vector2) -> bool:
    """Return true if map coordinates are an apple"""
    if gmap[int(pos.y)][int(pos.x)] == 'A':
        return True
    return False


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()
