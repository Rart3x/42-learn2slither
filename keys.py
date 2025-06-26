import pygame

from imports import *
from classes.Snake import Snake, SnakeBody, SnakeComponent, SnakeHead


def keys(key: pygame.key,  snake: Snake, now, last_move_time: int, running: bool) -> tuple[int, bool]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if snake.head.pos.y <= 0.0:
                exit()
            elif snake.head.orientation != "SOUTH":
                snake.move("NORTH")
                snake.head.orientation = "NORTH"

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if snake.head.pos.y >= GRID_ROWS - 1:
                exit()
            elif snake.head.orientation != "NORTH":
                snake.move("SOUTH")
                snake.head.orientation = "SOUTH"

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if snake.head.pos.x <= 0.0:
                exit()
            elif snake.head.orientation != "EAST":
                snake.move("WEST")
                snake.head.orientation = "WEST"

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if snake.head.pos.x >= GRID_COLS - 1:
                exit()
            elif snake.head.orientation != "WEST":
                snake.move("EAST")
                snake.head.orientation = "EAST"

        last_move_time = now

    return last_move_time, running