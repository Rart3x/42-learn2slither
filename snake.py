from typing import Any

import pygame
import random as rnd

GRID_COLS = 10
GRID_ROWS = 10

MOVE_DELAY = 75


def load_textures(cell_width: int, cell_height: int) -> dict[str, pygame.Surface]:
    """Load and return a dictionary of textures."""

    paths = {
        "BODY_TOP_LEFT": "assets/snake/body_top_left.png",
        "BODY_TOP_RIGHT": "assets/snake/body_top_right.png",

        "BODY_BOT_LEFT": "assets/snake/body_bot_left.png",
        "BODY_BOT_RIGHT": "assets/snake/body_bot_right.png",

        "BODY_HORIZONTAL": "assets/snake/body_horizontal.png",
        "BODY_VERTICAL": "assets/snake/body_vertical.png",

        "SNAKE_HEAD_UP": "assets/snake/head_up.png",
        "SNAKE_HEAD_DOWN": "assets/snake/head_down.png",
        "SNAKE_HEAD_LEFT": "assets/snake/head_left.png",
        "SNAKE_HEAD_RIGHT": "assets/snake/head_right.png",

        "TAIL_HEAD_UP": "assets/snake/tail_up.png",
        "TAIL_HEAD_DOWN": "assets/snake/tail_down.png",
        "TAIL_HEAD_LEFT": "assets/snake/tail_left.png",
        "TAIL_HEAD_RIGHT": "assets/snake/tail_right.png",

        "APPLE": "assets/components/apple.png",
        "BAD_APPLE": "assets/components/bad_apple.png",
    }

    textures = {}

    for key, path in paths.items():
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (cell_width, cell_height))
        textures[key] = img

    return textures


def print_map(gmap: list) -> None:
    """Display the map"""
    for row in gmap:
        print(" ".join(row))
    print()


def create_map() -> tuple[ pygame.Vector2, list[Any], pygame.Vector2]:
    """Create a randomize Snake map"""
    gmap = []

    head_x = rnd.randrange(10)
    head_y = rnd.randrange(10)

    while True:
        x2 = rnd.randrange(10)
        y2 = rnd.randrange(10)

        if x2 != head_x or y2 != head_y:
            break

    for y in range(GRID_ROWS):
        row = []

        for x in range(GRID_COLS):
            if x == head_x and y == head_y:
                row.append("H")
            elif x == x2 and y == y2:
                row.append("A")
            else:
                row.append("0")

        gmap.append(row)

    print_map(gmap)

    return pygame.Vector2(x2, y2), gmap, pygame.Vector2(head_x, head_y)


def keys(key: pygame.key, player_pos: pygame.Vector2, now, last_move_time: int, running: bool, snake_orientation: str) -> tuple[int, bool, str]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player_pos.y > 0.0:
                player_pos.y -= 1
                snake_orientation = "NORTH"

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if player_pos.y < GRID_ROWS - 1:
                player_pos.y += 1
                snake_orientation = "SOUTH"

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if player_pos.x > 0.0:
                player_pos.x -= 1
                snake_orientation = "WEST"

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player_pos.x < GRID_COLS - 1:
                player_pos.x += 1
                snake_orientation = "EAST"

        last_move_time = now

    return last_move_time, running, snake_orientation


def snake() -> None:
    """Snake function"""
    pygame.init()
    pygame.display.set_caption("🐍 Learn2Slither 🐍")

    screen = pygame.display.set_mode((1280, 720))

    clock = pygame.time.Clock()

    running = True

    CELL_WIDTH = screen.get_width() // GRID_COLS
    CELL_HEIGHT = screen.get_height() // GRID_ROWS

    textures = load_textures(CELL_WIDTH, CELL_HEIGHT)
    apple_pos, gmap, player_pos = create_map()

    last_move_time = pygame.time.get_ticks()

    snake_orientation = 'NORTH'

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        last_move_time, running, snake_orientation = keys(key, player_pos, now, last_move_time, running, snake_orientation)

        screen.fill("white")

        for y in range(GRID_ROWS):

            for x in range(GRID_COLS):
                pos_px = (x * CELL_WIDTH, y * CELL_HEIGHT)

                if x == int(player_pos.x) and y == int(player_pos.y):
                    if snake_orientation == 'NORTH':
                        screen.blit(textures["SNAKE_HEAD_UP"], pos_px)
                    elif snake_orientation == 'SOUTH':
                        screen.blit(textures["SNAKE_HEAD_DOWN"], pos_px)
                    elif snake_orientation == 'WEST':
                        screen.blit(textures["SNAKE_HEAD_LEFT"], pos_px)
                    elif snake_orientation == 'EAST':
                        screen.blit(textures["SNAKE_HEAD_RIGHT"], pos_px)

                elif x == int(apple_pos.x) and y == int(apple_pos.y):
                    screen.blit(textures["APPLE"], pos_px)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (pos_px[0], pos_px[1], CELL_WIDTH, CELL_HEIGHT))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()