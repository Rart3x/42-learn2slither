from keys import keys
from map import *
from classes.Snake import Snake
from textures import *
from utils import is_there_apple, is_there_malus


def snake() -> None:
    """Snake function"""
    pygame.init()
    pygame.display.set_caption("🐍 Learn2Slither 🐍")

    screen = pygame.display.set_mode((750, 750))

    clock = pygame.time.Clock()

    running = True

    CELL_WIDTH = screen.get_width() // GRID_COLS
    CELL_HEIGHT = screen.get_height() // GRID_ROWS

    textures = load_textures(CELL_WIDTH, CELL_HEIGHT)
    gmap, player_pos = create_map()

    snake = Snake(player_pos)
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
        last_move_time, running = keys(key, gmap, snake, now, last_move_time, running)

        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                pos_px = (x * CELL_WIDTH, y * CELL_HEIGHT)

                if (x + y) % 2 == 0:
                    color = GREEN_LIGHT
                else:
                    color = GREEN_DARK

                pygame.draw.rect(screen, color, (pos_px[0], pos_px[1], CELL_WIDTH, CELL_HEIGHT))

        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                pos_px = (x * CELL_WIDTH, y * CELL_HEIGHT)

                if x == snake.head.pos.x and y == snake.head.pos.y:
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
                    index = snake.components.index(comp)

                    # Queue segment (last component)
                    if index == len(snake.components) - 1 and index != 0:
                        prev = snake.components[index - 1]
                        dir_prev = comp.pos - prev.pos

                        if dir_prev == pygame.Vector2(0, -1):
                            screen.blit(textures["TAIL_HEAD_UP"], pos_px)
                        elif dir_prev == pygame.Vector2(0, 1):
                            screen.blit(textures["TAIL_HEAD_DOWN"], pos_px)
                        elif dir_prev == pygame.Vector2(-1, 0):
                            screen.blit(textures["TAIL_HEAD_LEFT"], pos_px)
                        elif dir_prev == pygame.Vector2(1, 0):
                            screen.blit(textures["TAIL_HEAD_RIGHT"], pos_px)

                    # Body bends (not head or tail)
                    elif 0 < index < len(snake.components) - 1:
                        prev = snake.components[index - 1]
                        next = snake.components[index + 1]

                        dir_prev = comp.pos - prev.pos
                        dir_next = comp.pos - next.pos

                        dirs = {
                            (0, -1): "N",
                            (0, 1): "S",
                            (-1, 0): "W",
                            (1, 0): "E"
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
                            if comp.orientation in ("NORTH", "SOUTH"):
                                screen.blit(textures["BODY_VERTICAL"], pos_px)
                            else:
                                screen.blit(textures["BODY_HORIZONTAL"], pos_px)

                    # Straight body parts (first after head or single segment)
                    else:
                        if comp.orientation in ("NORTH", "SOUTH"):
                            screen.blit(textures["BODY_VERTICAL"], pos_px)
                        else:
                            screen.blit(textures["BODY_HORIZONTAL"], pos_px)

                elif is_there_apple(gmap, pygame.Vector2(x, y)):
                    screen.blit(textures["APPLE"], pos_px)
                elif is_there_malus(gmap, pygame.Vector2(x, y)):
                    screen.blit(textures["MALUS"], pos_px)

        pygame.display.flip()

        clock.tick(60)

        if snake.off:
            exit()

    pygame.quit()