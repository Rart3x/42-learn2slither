import pygame


def find_element_in_list(lst : list, element: str) -> pygame.Vector2:
    """Find the element in a list."""
    for el in lst:
        if el == element:
            return el
    return pygame.Vector2(0, 0)


def is_there_apple(gmap: list, pos: pygame.Vector2) -> bool:
    """Return true if map coordinates are an apple"""
    if gmap[int(pos.y)][int(pos.x)] == 'G':
        return True
    return False


def is_there_malus(gmap: list, pos: pygame.Vector2) -> bool:
    """Return true if map coordinates are an apple"""
    if gmap[int(pos.y)][int(pos.x)] == 'R':
        return True
    return False


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()
