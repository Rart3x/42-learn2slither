import pygame

from classes.Button import Button
from imports import BLUE, WHITE, GRID_COLS, GRID_ROWS, GREEN_LIGHT, GREEN_DARK
from map import create_map
from snake import snake
from textures import load_textures


def menu(screen) -> None:
    """
    Main menu loop displaying title and buttons.
    Handles navigation between menu and the snake game.
    """
    title = pygame.font.SysFont("Arial", 64)

    clock = pygame.time.Clock()

    cell_width = screen.get_width() // GRID_COLS
    cell_height = screen.get_height() // GRID_ROWS

    textures = load_textures(cell_width, cell_height)
    gmap, player_pos = create_map()


    running = True
    in_game = False

    def start_game():
        """Callback to start the snake game."""
        nonlocal in_game
        in_game = True

    def quit_game():
        """Callback to quit the game and exit."""
        pygame.quit()
        exit()

    buttons = [
        Button("Play", (screen.get_height() // 2 - 100, 250), (200, 60), start_game),
        Button("Quit", (screen.get_height() // 2 - 100, 340), (200, 60), quit_game),
    ]

    focused_button = 0  # Index of focused button
    buttons[focused_button].focused = True

    while running:
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_game()

                    if event.key in (pygame.K_UP, pygame.K_w):
                        # Move focus up
                        buttons[focused_button].focused = False
                        focused_button = (focused_button - 1) % len(buttons)
                        buttons[focused_button].focused = True

                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        # Move focus down
                        buttons[focused_button].focused = False
                        focused_button = (focused_button + 1) % len(buttons)
                        buttons[focused_button].focused = True

                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        # Activate focused button
                        buttons[focused_button].callback()

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
