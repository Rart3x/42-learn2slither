import pygame

from classes.Snake import Snake
from imports import GRID_COLS, GRID_ROWS, MOVE_DELAY
from map import create_new_apple, create_new_malus
from utils import is_there_apple, is_there_malus


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
    create_malus_func,
    running: bool
):
    """
    General handler for directional movement, interactions, and map updates.
    """
    pos_val = snake.head.pos.y if axis == "y" else snake.head.pos.x

    if (
        (axis == "y" and direction == "NORTH" and pos_val <= 0)
        or (axis == "y" and direction == "SOUTH"
            and pos_val >= grid_limit - 1)
        or (axis == "x" and direction == "WEST" and pos_val <= 0)
        or (axis == "x" and direction == "EAST"
            and pos_val >= grid_limit - 1)
    ):
        return False

    if can_change_direction(snake.head.orientation, direction):
        next_pos = snake.head.pos + move_vec
        ate_apple, ate_malus, running = handle_next_tile(gmap, snake, next_pos, running)

        if not running:
            return False

        if not snake.move(direction):
            return False
        
        snake.head.orientation = direction

        if ate_apple:
            create_apple_func(snake, gmap)
        if ate_malus:
            create_malus_func(snake, gmap)

    return True


def handle_next_tile(
    gmap: list,
    snake: Snake,
    next_pos: pygame.Vector2,
    running: bool
) -> tuple[bool, bool, bool]:
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
        running = snake.shrink()
        ate_malus = True

    return ate_apple, ate_malus, running


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
        if key[pygame.K_w]:
            running = handle_directional_move(
                snake, gmap, "NORTH", pygame.Vector2(0, -1),
                GRID_ROWS, "y", create_new_apple, create_new_malus, running
            )

        elif key[pygame.K_s]:
            running = handle_directional_move(
                snake, gmap, "SOUTH", pygame.Vector2(0, 1),
                GRID_ROWS, "y", create_new_apple, create_new_malus, running
            )
        elif key[pygame.K_a]:
            running = handle_directional_move(
                snake, gmap, "WEST", pygame.Vector2(-1, 0),
                GRID_COLS, "x", create_new_apple, create_new_malus, running
            )
        elif key[pygame.K_d]:
            running = handle_directional_move(
                snake, gmap, "EAST", pygame.Vector2(1, 0),
                GRID_COLS, "x", create_new_apple, create_new_malus, running
            )

        last_move_time = now

    return last_move_time, running
