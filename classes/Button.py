import pygame

from imports import GRID_COLS, GRID_ROWS, GREEN_LIGHT, GREEN_DARK


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