from imports import *


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()


def find_snake_head(gmap: list) -> tuple[int, int]:
    """Return a tuple of snake head coordinates"""
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if gmap[y][x] == 'H':
                return y, x
    return 0, 0
