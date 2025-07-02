import pygame
import random as rnd

from classes.Snake import Snake
from imports import GRID_COLS, GRID_ROWS
from typing import Any


def create_map() -> tuple[list[Any], pygame.Vector2]:
    """Create a randomized Snake map."""
    gmap = []

    head_x = rnd.randrange(10)
    head_y = rnd.randrange(10)

    # Create a random apple
    while True:
        x2 = rnd.randrange(10)
        y2 = rnd.randrange(10)
        if x2 != head_x or y2 != head_y:
            break

    while True:
        x3 = rnd.randrange(10)
        y3 = rnd.randrange(10)
        if (x3, y3) != (head_x, head_y) and (x3, y3) != (x2, y2):
            break

    while True:
        x4 = rnd.randrange(10)
        y4 = rnd.randrange(10)
        if (
            (x4, y4) != (head_x, head_y)
            and (x4, y4) != (x2, y2)
            and (x4, y4) != (x3, y3)
        ):
            break

    for y in range(GRID_ROWS):
        row = []
        for x in range(GRID_COLS):
            row.append("0")
        gmap.append(row)

    gmap[y2][x2] = "G"
    gmap[y3][x3] = "G"
    gmap[y4][x4] = "R"

    return gmap, pygame.Vector2(head_x, head_y)


def create_new_apple(snake: Snake, gmap: list):
    """
    Create a new apple at a random position not occupied by the snake.
    Removes the one possibly created under the head.
    """
    gmap[int(snake.head.pos.y)][int(snake.head.pos.x)] = "0"

    height = len(gmap)
    width = len(gmap[0]) if height > 0 else 0

    while True:
        x = rnd.randint(0, width - 1)
        y = rnd.randint(0, height - 1)
        pos = pygame.Vector2(x, y)

        if gmap[y][x] == "0" and not snake.has_component_at(pos):
            gmap[y][x] = "G"
            break


def create_new_malus(snake: Snake, gmap: list):
    """
    Create a new malus at a random position not occupied by the snake.
    Removes the one possibly created under the head.
    """
    gmap[int(snake.head.pos.y)][int(snake.head.pos.x)] = "0"

    height = len(gmap)
    width = len(gmap[0]) if height > 0 else 0

    while True:
        x = rnd.randint(0, width - 1)
        y = rnd.randint(0, height - 1)
        pos = pygame.Vector2(x, y)

        if gmap[y][x] == "0" and not snake.has_component_at(pos):
            gmap[y][x] = "R"
            break


def create_snake_body(
    gmap: list,
    pos: pygame.Vector2
) -> tuple[list[pygame.Vector2], str]:
    """
    Create a snake body with valid coordinates
    and return them with orientation.
    """
    height = len(gmap)
    width = len(gmap[0]) if height > 0 else 0

    directions = []

    x = int(pos.x)
    y = int(pos.y)

    # Check NORTH (body extends downward on the map)
    if (
        y + 2 < height
        and gmap[y + 1][x] == '0'
        and gmap[y + 2][x] == '0'
    ):
        directions.append((
            "NORTH",
            [pygame.Vector2(x, y + 1), pygame.Vector2(x, y + 2)]
        ))

    # Check SOUTH (body extends upward on the map)
    if (
        y - 2 >= 0
        and gmap[y - 1][x] == '0'
        and gmap[y - 2][x] == '0'
    ):
        directions.append((
            "SOUTH",
            [pygame.Vector2(x, y - 1), pygame.Vector2(x, y - 2)]
        ))

    # Check WEST (body extends to the right on the map)
    if (
        x + 2 < width
        and gmap[y][x + 1] == '0'
        and gmap[y][x + 2] == '0'
    ):
        directions.append((
            "WEST",
            [pygame.Vector2(x + 1, y), pygame.Vector2(x + 2, y)]
        ))

    # Check EAST (body extends to the left on the map)
    if (
        x - 2 >= 0
        and gmap[y][x - 1] == '0'
        and gmap[y][x - 2] == '0'
    ):
        directions.append((
            "EAST",
            [pygame.Vector2(x - 1, y), pygame.Vector2(x - 2, y)]
        ))

    orientation, body_coords = rnd.choice(directions)
    return body_coords, orientation
