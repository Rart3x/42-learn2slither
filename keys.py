import pygame

from imports import *
from classes.Snake import Snake, SnakeBody, SnakeComponent, SnakeHead


def keys(key: pygame.key,  head: SnakeHead, now, last_move_time: int, running: bool) -> tuple[int, bool]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if head.pos.y > 0.0:
                head.pos.y -= 1
                head.orientation = "NORTH"

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if head.pos.y < GRID_ROWS - 1:
                head.pos.y += 1
                head.orientation = "SOUTH"

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if head.pos.x > 0.0:
                head.pos.x -= 1
                head.orientation = "WEST"

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if head.pos.x < GRID_COLS - 1:
                head.pos.x += 1
                head.orientation = "EAST"

        last_move_time = now

    return last_move_time, running