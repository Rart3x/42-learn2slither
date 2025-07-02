import pygame

from imports import GREEN_DARK, GREEN_LIGHT, GRID_COLS, GRID_ROWS
from keys import keys
from map import create_map, create_snake_body
from classes.Snake import Snake
from textures import load_textures
from utils import is_there_apple, is_there_malus


def snake(screen, textures) -> bool:
    clock = pygame.time.Clock()
    running = True

    cell_width = screen.get_width() // GRID_COLS
    cell_height = screen.get_height() // GRID_ROWS

    gmap, player_pos = create_map()

    snake = Snake(player_pos)
    body, orientations = create_snake_body(gmap, snake.head.pos)

    snake.head.orientation = orientations
    snake.add_component(body[0], orientations)
    snake.add_component(body[1], orientations)

    snake.view(gmap)

    last_move_time = pygame.time.get_ticks()

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        key = pygame.key.get_pressed()
        last_move_time, running = keys(key, gmap,
                                       snake, now, last_move_time, running)

        # Draw background
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                pos_px = (x * cell_width, y * cell_height)
                color = GREEN_LIGHT if (x + y) % 2 == 0 else GREEN_DARK
                pygame.draw.rect(screen, color,
                                 (pos_px[0], pos_px[1],
                                  cell_width, cell_height))

        # Draw elements
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                pos_px = (x * cell_width, y * cell_height)
                pos_vec = pygame.Vector2(x, y)

                if x == snake.head.pos.x and y == snake.head.pos.y:
                    head_tex = {
                        'NORTH': "SNAKE_HEAD_UP",
                        'SOUTH': "SNAKE_HEAD_DOWN",
                        'WEST': "SNAKE_HEAD_LEFT",
                        'EAST': "SNAKE_HEAD_RIGHT"
                    }.get(snake.head.orientation)

                    if head_tex:
                        screen.blit(textures[head_tex], pos_px)

                elif snake.has_component_at(pos_vec):
                    comp = snake.get_component_at(pos_vec)
                    index = snake.components.index(comp)

                    if index == len(snake.components) - 1 and index != 0:
                        prev = snake.components[index - 1]
                        dir_prev = comp.pos - prev.pos
                        tail_map = {
                            (0, -1): "TAIL_HEAD_UP",
                            (0, 1): "TAIL_HEAD_DOWN",
                            (-1, 0): "TAIL_HEAD_LEFT",
                            (1, 0): "TAIL_HEAD_RIGHT"
                        }
                        key = (int(dir_prev.x), int(dir_prev.y))
                        screen.blit(textures.get(tail_map.get(key, ""),
                                                 None), pos_px)

                    elif 0 < index < len(snake.components) - 1:
                        prev = snake.components[index - 1]
                        next = snake.components[index + 1]
                        dir_prev = comp.pos - prev.pos
                        dir_next = comp.pos - next.pos

                        dirs = {
                            (0, -1): "N", (0, 1): "S",
                            (-1, 0): "W", (1, 0): "E"
                        }

                        d1 = dirs.get((int(dir_prev.x), int(dir_prev.y)))
                        d2 = dirs.get((int(dir_next.x), int(dir_next.y)))

                        turn_key = {
                            frozenset(["N", "E"]): "BODY_BOT_LEFT",
                            frozenset(["N", "W"]): "BODY_BOT_RIGHT",
                            frozenset(["S", "E"]): "BODY_TOP_LEFT",
                            frozenset(["S", "W"]): "BODY_TOP_RIGHT"
                        }

                        turn = turn_key.get(frozenset([d1, d2]))

                        if turn:
                            screen.blit(textures[turn], pos_px)
                        else:
                            tex = "BODY_VERTICAL" \
                                if comp.orientation in ("NORTH", "SOUTH") \
                                else "BODY_HORIZONTAL"
                            screen.blit(textures[tex], pos_px)

                    else:
                        tex = "BODY_VERTICAL" \
                            if comp.orientation in ("NORTH", "SOUTH") \
                            else "BODY_HORIZONTAL"
                        screen.blit(textures[tex], pos_px)

                elif is_there_apple(gmap, pos_vec):
                    screen.blit(textures["APPLE"], pos_px)
                elif is_there_malus(gmap, pos_vec):
                    screen.blit(textures["MALUS"], pos_px)

        pygame.display.flip()
        clock.tick(60)

        snake.view(gmap)

        if snake.off:
            return True  # Return to menu

    return True
