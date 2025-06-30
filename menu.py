import pygame
from snake import snake


def menu(screen) -> None:
    WHITE = (255, 255, 255)
    GREY = (200, 200, 200)
    DARK_GREY = (100, 100, 100)
    BLACK = (0, 0, 0)
    BLUE = (70, 130, 180)

    TITLE_FONT = pygame.font.SysFont("Arial", 64)
    BUTTON_FONT = pygame.font.SysFont("Arial", 32)

    class Button:
        def __init__(self, text, pos, size, callback):
            self.text = text
            self.rect = pygame.Rect(pos, size)
            self.callback = callback
            self.hovered = False

        def draw(self, surface):
            color = DARK_GREY if self.hovered else GREY
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

            text_surf = BUTTON_FONT.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

        def update(self, mouse_pos, mouse_pressed):
            self.hovered = self.rect.collidepoint(mouse_pos)
            if self.hovered and mouse_pressed[0]:
                self.callback()

    clock = pygame.time.Clock()

    running = True
    in_game = False

    def start_game():
        nonlocal in_game
        in_game = True

    def quit_game():
        pygame.quit()
        exit()

    buttons = [
        Button("Play", (750 // 2 - 100, 250), (200, 60), start_game),
        Button("Quit", (750 // 2 - 100, 340), (200, 60), quit_game)
    ]

    while running:
        if not in_game:
            screen.fill(BLUE)
            title_surf = TITLE_FONT.render("Learn2Slither", True, WHITE)
            title_rect = title_surf.get_rect(center=(750 // 2, 120))
            screen.blit(title_surf, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

            for button in buttons:
                button.update(mouse_pos, mouse_pressed)
                button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        else:
            # Launch snake game loop; returns False if user quits, True to go back to menu
            back_to_menu = snake(screen)

            if not back_to_menu:
                running = False
            else:
                in_game = False
