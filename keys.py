import pygame

from classes.Snake import Snake
from imports import *
from map import create_new_apple, create_new_malus
from utils import *


def can_change_direction(current: str, new: str) -> bool:
    """
    Prevents 180° turns (e.g., NORTH <-> SOUTH).
    """
    opposites = {
        "NORTH": "SOUTH",
        "SOUTH": "NORTH",
        "EAST": "WEST",
        "WEST": "EAST"
    }
    return current != opposites.get(new)


def handle_directional_move(
    snake: Snake,
    gmap: list,
    direction: str,
    move_vec: pygame.Vector2,
    grid_limit: int,
    axis: str,
    create_apple_func,
    create_malus_func
):
    """
    General handler for directional movement, interactions, and map updates.
    """
    pos_val = snake.head.pos.y if axis == "y" else snake.head.pos.x
    if (axis == "y" and (direction == "NORTH" and pos_val <= 0)) or \
       (axis == "y" and (direction == "SOUTH" and pos_val >= grid_limit - 1)) or \
       (axis == "x" and (direction == "WEST" and pos_val <= 0)) or \
       (axis == "x" and (direction == "EAST" and pos_val >= grid_limit - 1)):
        exit()

    if can_change_direction(snake.head.orientation, direction):
        next_pos = snake.head.pos + move_vec
        ate_apple, ate_malus = handle_next_tile(gmap, snake, next_pos)

        snake.move(direction)
        snake.head.orientation = direction

        if ate_apple:
            create_apple_func(snake, gmap)
        if ate_malus:
            create_malus_func(snake, gmap)


def handle_next_tile(gmap: list, snake: Snake, next_pos: pygame.Vector2) -> tuple[bool, bool]:
    """
    Check what's on the next tile and handle snake reaction (grow/shrink).
    Returns a tuple: (ate_apple, ate_malus)
    """
    ate_apple = False
    ate_malus = False

    if is_there_apple(gmap, next_pos):
        snake.play_crunch()
        snake.grow()
        ate_apple = True

    if is_there_malus(gmap, next_pos):
        snake.play_crunch()
        snake.shrink()
        ate_malus = True

    return ate_apple, ate_malus


def keys(
    key: pygame.key,
    gmap: list,
    snake: Snake,
    now,
    last_move_time: int,
    running: bool
) -> tuple[int, bool]:
    """
    Global keyboard handler that maps keys to snake movement and game events.
    """
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:
        if key[pygame.K_w] or key[pygame.K_UP]:
            handle_directional_move(snake, gmap, "NORTH", pygame.Vector2(0, -1), GRID_ROWS, "y", create_new_apple, create_new_malus)
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            handle_directional_move(snake, gmap, "SOUTH", pygame.Vector2(0, 1), GRID_ROWS, "y", create_new_apple, create_new_malus)
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            handle_directional_move(snake, gmap, "WEST", pygame.Vector2(-1, 0), GRID_COLS, "x", create_new_apple, create_new_malus)
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            handle_directional_move(snake, gmap, "EAST", pygame.Vector2(1, 0), GRID_COLS, "x", create_new_apple, create_new_malus)

        last_move_time = now

    return last_move_time, running
