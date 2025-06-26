import pygame

from imports import *
from keys import keys
from map import *
from classes.Snake import Snake
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
    gmap, player_pos = create_map()

    snake = Snake(player_pos, "NORTH")
    body, orientations = create_snake_body(gmap, snake.head.pos)

    snake.head.orientation = orientations
    snake.add_component(body[0], orientations)
    snake.add_component(body[1], orientations)

    last_move_time = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        last_move_time, running = keys(key, snake.head, now, last_move_time, running)

        screen.fill("white")

        for y in range(GRID_ROWS):

            for x in range(GRID_COLS):
                pos_px = (x * CELL_WIDTH, y * CELL_HEIGHT)

                if x == int(player_pos.x) and y == int(player_pos.y):
                    if snake.head.orientation == 'NORTH':
                        screen.blit(textures["SNAKE_HEAD_UP"], pos_px)
                    elif snake.head.orientation == 'SOUTH':
                        screen.blit(textures["SNAKE_HEAD_DOWN"], pos_px)
                    elif snake.head.orientation == 'WEST':
                        screen.blit(textures["SNAKE_HEAD_LEFT"], pos_px)
                    elif snake.head.orientation == 'EAST':
                        screen.blit(textures["SNAKE_HEAD_RIGHT"], pos_px)

                elif snake.has_component_at(pygame.Vector2(x, y)):
                    comp = snake.get_component_at(pygame.Vector2(x, y))

                    if comp.orientation in ("NORTH", "SOUTH"):
                        screen.blit(textures["BODY_VERTICAL"], pos_px)
                    elif comp.orientation in ("WEST", "EAST"):
                        screen.blit(textures["BODY_HORIZONTAL"], pos_px)

                elif is_there_apple(gmap, pygame.Vector2(x, y)):
                    screen.blit(textures["APPLE"], pos_px)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (pos_px[0], pos_px[1], CELL_WIDTH, CELL_HEIGHT))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()