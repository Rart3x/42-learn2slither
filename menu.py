import pygame

from classes.Button import Button
from classes.Snake import Snake
from imports import BLUE, WHITE, GRID_COLS, GRID_ROWS, GREEN_LIGHT, GREEN_DARK
from keys import keys
from map import create_map, create_snake_body
from snake import snake
from textures import load_textures
from utils import is_there_apple, is_there_malus


def menu(screen) -> None:
    """
    Main menu loop displaying title and buttons.
    Handles navigation between menu and the snake_obj game.
    """
    def start_game():
        """Callback to start the snake_obj game."""
        nonlocal in_game
        in_game = True

    def quit_game():
        """Callback to quit the game and exit."""
        pygame.quit()
        exit()

    def reset_simulation():
        """Initialize map and snake for menu simulation."""
        nonlocal gmap, snake_obj, last_move_time
        gmap, player_pos = create_map()
        snake_obj = Snake(player_pos)
        body, orientations = create_snake_body(gmap, snake_obj.head.pos)
        snake_obj.head.orientation = orientations
        snake_obj.add_component(body[0], orientations)
        snake_obj.add_component(body[1], orientations)
        last_move_time = pygame.time.get_ticks()

    title = pygame.font.SysFont("Arial", 64)

    clock = pygame.time.Clock()

    cell_width = screen.get_width() // GRID_COLS
    cell_height = screen.get_height() // GRID_ROWS

    textures = load_textures(cell_width, cell_height)
    gmap, player_pos = create_map()

    snake_obj = Snake(player_pos)
    body, orientations = create_snake_body(gmap, snake_obj.head.pos)

    snake_obj.head.orientation = orientations
    snake_obj.add_component(body[0], orientations)
    snake_obj.add_component(body[1], orientations)

    last_move_time = pygame.time.get_ticks()

    in_game = False
    running = True
    simulation = True

    buttons = [
        Button("Play", (screen.get_height() // 2 - 100, 250), (200, 60), start_game),
        Button("Quit", (screen.get_height() // 2 - 100, 340), (200, 60), quit_game),
    ]

    focused_button = 0  # Index of focused button
    buttons[focused_button].focused = True

    while running:
        now = pygame.time.get_ticks()

        if not in_game:
            screen.fill(BLUE)
            title_surf = title.render("Learn2Slither", True, WHITE)
            title_rect = title_surf.get_rect(center=(750 // 2, 120))
            screen.blit(title_surf, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # Draw grid background
            for y in range(GRID_ROWS):
                for x in range(GRID_COLS):
                    pos_px = (x * cell_width, y * cell_height)
                    color = GREEN_LIGHT if (x + y) % 2 == 0 else GREEN_DARK
                    pygame.draw.rect(screen, color,
                                    (pos_px[0], pos_px[1],
                                    cell_width, cell_height))

            for y in range(GRID_ROWS):
                for x in range(GRID_COLS):
                    pos_px = (x * cell_width, y * cell_height)
                    pos_vec = pygame.Vector2(x, y)

                    if x == snake_obj.head.pos.x and y == snake_obj.head.pos.y:
                        head_tex = {
                            'NORTH': "SNAKE_HEAD_UP",
                            'SOUTH': "SNAKE_HEAD_DOWN",
                            'WEST': "SNAKE_HEAD_LEFT",
                            'EAST': "SNAKE_HEAD_RIGHT"
                        }.get(snake_obj.head.orientation)

                        if head_tex:
                            screen.blit(textures[head_tex], pos_px)

                    elif snake_obj.has_component_at(pos_vec):
                        comp = snake_obj.get_component_at(pos_vec)
                        index = snake_obj.components.index(comp)

                        if index == len(snake_obj.components) - 1 and index != 0:
                            prev = snake_obj.components[index - 1]
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

                        elif 0 < index < len(snake_obj.components) - 1:
                            prev = snake_obj.components[index - 1]
                            next = snake_obj.components[index + 1]
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_game()

                    if event.key == pygame.K_UP:
                        # Move focus up
                        buttons[focused_button].focused = False
                        focused_button = (focused_button - 1) % len(buttons)
                        buttons[focused_button].focused = True

                    elif event.key == pygame.K_DOWN:
                        # Move focus down
                        buttons[focused_button].focused = False
                        focused_button = (focused_button + 1) % len(buttons)
                        buttons[focused_button].focused = True

                    elif event.key == pygame.K_RETURN:
                        # Activate focused button
                        buttons[focused_button].callback()

            key = pygame.key.get_pressed()
            last_move_time, simulation = keys(key, gmap, snake_obj, now, last_move_time, simulation)

            if not simulation:
                reset_simulation()
                simulation = True

            # Update buttons: hover with mouse, but only if mouse not moved away from focused
            for i, button in enumerate(buttons):
                if i != focused_button:
                    button.update(mouse_pos, mouse_pressed)
                else:
                    button.hovered = False  # Prevent hover override on focused button

                button.draw(screen)

            pygame.display.flip()
            
            clock.tick(60)

        else:
            back_to_menu = snake(screen, textures)

            if not back_to_menu:
                running = False
            else:
                in_game = False
                reset_simulation()
