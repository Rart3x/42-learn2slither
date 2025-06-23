from typing import Any

import pygame
import random as rnd

GRID_COLS = 10
GRID_ROWS = 10

MOVE_DELAY = 75


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()


def create_map() -> tuple[list[Any], pygame.Vector2]:
    """Create a randomize Snake map"""
    gmap = []

    head_x = rnd.randrange(10)
    head_y = rnd.randrange(10)

    for y in range(GRID_ROWS):
        row = []

        for x in range(GRID_COLS):
            if x == head_x and y == head_y:
                row.append("H")
            else:
                row.append("0")

        gmap.append(row)

    print_map(gmap)

    return gmap, pygame.Vector2(head_x, head_y)


def keys(key: pygame.key, player_pos: pygame.Vector2, now, last_move_time: int, running: bool) -> tuple[int, bool]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player_pos.y > 0.0:
                player_pos.y -= 1

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if player_pos.y < GRID_ROWS - 1:
                player_pos.y += 1

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if player_pos.x > 0.0:
                player_pos.x -= 1

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player_pos.x < GRID_COLS - 1:
                player_pos.x += 1

        last_move_time = now

    return last_move_time, running


def snake() -> None:
    """Snake function"""
    pygame.init()
    pygame.display.set_caption("🐍 Learn2Slither 🐍")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    CELL_WIDTH = screen.get_width() // GRID_COLS
    CELL_HEIGHT = screen.get_height() // GRID_ROWS

    texture = pygame.image.load("assets/snake/head_up.png")
    texture = pygame.transform.scale(texture, (CELL_WIDTH, CELL_HEIGHT))

    gmap, player_pos = create_map()

    last_move_time = pygame.time.get_ticks()

    while running:

        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        last_move_time, running = keys(key, player_pos, now, last_move_time, running)

        screen.fill("white")

        for y in range(GRID_ROWS):

            for x in range(GRID_COLS):
                pos_px = (x * CELL_WIDTH, y * CELL_HEIGHT)

                if x == int(player_pos.x) and y == int(player_pos.y):
                    screen.blit(texture, pos_px)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (pos_px[0], pos_px[1], CELL_WIDTH, CELL_HEIGHT))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()