import pygame

from imports import *


def is_there_apple(gmap: list, pos: pygame.Vector2) -> bool:
    """Return true if map coordinates are an apple"""
    if gmap[int(pos.y)][int(pos.x)] == 'A':
        return True
    return False


def is_there_malus(gmap: list, pos: pygame.Vector2) -> bool:
    """Return true if map coordinates are an apple"""
    if gmap[int(pos.y)][int(pos.x)] == 'M':
        return True
    return False


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()
