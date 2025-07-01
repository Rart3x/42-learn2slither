import pygame

class Button:
    """
    Button UI element with hover and click functionality.
    Supports transparency and rounded corners.
    """
    def __init__(self, text, pos, size, callback):
        """
        Initialize a button.
        """
        self.text = text
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.callback = callback
        self.hovered = False
        self.focused = False  # Focus state for keyboard navigation
        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self, surface):
        """
        Draw the button on the given surface with transparency and styles.
        """
        # Create transparent button surface
        button_surf = pygame.Surface(self.size, pygame.SRCALPHA)

        # Define base colors with alpha
        normal_color = (255, 255, 255, 80)
        hover_color = (255, 255, 255, 120)
        focus_color = (255, 255, 255, 160)

        if self.focused:
            fill_color = focus_color
        elif self.hovered:
            fill_color = hover_color
        else:
            fill_color = normal_color

        # Draw rounded rect on transparent surface
        pygame.draw.rect(button_surf, fill_color, button_surf.get_rect(), border_radius=12)

        # Draw border (opaque)
        pygame.draw.rect(button_surf, (0, 0, 0), button_surf.get_rect(), width=2, border_radius=12)

        # Render text
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(self.size[0] // 2, self.size[1] // 2))

        # Blit text on the button surface
        button_surf.blit(text_surf, text_rect)

        # Blit final button on screen
        surface.blit(button_surf, self.pos)

    def update(self, mouse_pos, mouse_pressed):
        """
        Update button hover state and trigger callback on click.
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_pressed[0]:
            self.callback()
