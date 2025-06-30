import pygame

from imports import BLUE, WHITE
from snake import snake


class Button:
    """
    Button UI element with hover and click functionality.
    """
    def __init__(self, text, pos, size, callback):
        """
        Initialize a button.
        """
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.callback = callback
        self.hovered = False
        self.focused = False  # Focus state for keyboard navigation

    def draw(self, surface):
        """
        Draw the button on the given surface.
        """
        if self.focused:
            color = (100, 150, 255)  # Light blue when focused
        else:
            color = (100, 100, 100) if self.hovered else (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        text_surf = (pygame.font.SysFont("Arial", 32)
                     .render(self.text, True, (0, 0, 0)))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos, mouse_pressed):
        """
        Update button hover state and trigger callback on click.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_pressed[0]:
            self.callback()


def menu(screen) -> None:
    """
    Main menu loop displaying title and buttons.
    Handles navigation between menu and the snake game.
    """
    title = pygame.font.SysFont("Arial", 64)

    clock = pygame.time.Clock()

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
        Button("Play", (750 // 2 - 100, 250), (200, 60), start_game),
        Button("Quit", (750 // 2 - 100, 340), (200, 60), quit_game),
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
            back_to_menu = snake(screen)

            if not back_to_menu:
                running = False
            else:
                in_game = False
