import random as rnd

from imports import *
from keys import *
from map import *
from textures import *


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