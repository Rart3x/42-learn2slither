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


def find_snake_head(gmap: list) -> tuple[int, int]:
    """Return a tuple of snake head coordinates"""
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if gmap[y][x] == 'H':
                return y, x
    return 0, 0


def create_map() -> tuple[ pygame.Vector2, list[Any], pygame.Vector2, str]:
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
            row.append("0")

        gmap.append(row)

    gmap[head_y][head_x] = "H"
    gmap[y2][x2] = "A"

    gmap, snake_orientation = create_snake_body(gmap)

    print_map(gmap)

    return pygame.Vector2(x2, y2), gmap, pygame.Vector2(head_x, head_y), snake_orientation


def create_snake_body(gmap: list) -> tuple[list, str]:
    """Add snake body on gmap, choosing a valid direction randomly if multiple options are available."""
    head_y, head_x = find_snake_head(gmap)
    height = len(gmap)
    width = len(gmap[0]) if height > 0 else 0

    directions = []

    # Check NORTH (body down from head)
    if head_y + 2 < height and gmap[head_y + 1][head_x] == '0' and gmap[head_y + 2][head_x] == '0':
        directions.append(("NORTH", [(head_y + 1, head_x), (head_y + 2, head_x)]))

    # Check SOUTH (body up from head)
    if head_y - 2 >= 0 and gmap[head_y - 1][head_x] == '0' and gmap[head_y - 2][head_x] == '0':
        directions.append(("SOUTH", [(head_y - 1, head_x), (head_y - 2, head_x)]))

    # Check WEST (body right from head)
    if head_x + 2 < width and gmap[head_y][head_x + 1] == '0' and gmap[head_y][head_x + 2] == '0':
        directions.append(("WEST", [(head_y, head_x + 1), (head_y, head_x + 2)]))

    # Check EAST (body left from head)
    if head_x - 2 >= 0 and gmap[head_y][head_x - 1] == '0' and gmap[head_y][head_x - 2] == '0':
        directions.append(("EAST", [(head_y, head_x - 1), (head_y, head_x - 2)]))

    if not directions:
        # No valid direction to place the body
        return gmap, ""

    # Choose one random valid direction
    chosen_direction, body_coords = rnd.choice(directions)

    # Apply body on the map
    for y, x in body_coords:
        gmap[y][x] = 'B'

    return gmap, chosen_direction


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
    apple_pos, gmap, player_pos, snake_orientation = create_map()

    last_move_time = pygame.time.get_ticks()

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

                elif gmap[y][x] == 'B':
                    if snake_orientation == "NORTH" or snake_orientation == "SOUTH":
                        screen.blit(textures["BODY_VERTICAL"], pos_px)
                    elif snake_orientation == "WEST" or snake_orientation == "EAST":
                        screen.blit(textures["BODY_HORIZONTAL"], pos_px)
                elif x == int(apple_pos.x) and y == int(apple_pos.y):
                    screen.blit(textures["APPLE"], pos_px)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (pos_px[0], pos_px[1], CELL_WIDTH, CELL_HEIGHT))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()