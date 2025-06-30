import pygame


class Snake:
    """Snake class"""

    def __init__(self, initial_pos: pygame.Vector2, orientation="NORTH"):
        """Snake constructor"""
        self.head = SnakeHead(initial_pos, orientation)

        self.components: list[SnakeComponent] = [
            self.head
        ]
        self.crunch = pygame.mixer.Sound('./assets/sounds/crunch.wav')
        self.positions: list[pygame.Vector2] = [initial_pos]
        self.off = False

    def add_component(self, pos: pygame.Vector2, orientation: str):
        """Add a new component at the end of the snake tail"""
        new_component = SnakeBody(pos, orientation)

        self.components.append(new_component)
        self.positions.append(pos)

    def get_component_at(self, pos: pygame.Vector2):
        """Return SnakeComponent that is in 'pos' coordinates"""
        if self.has_component_at(pos):
            for comp in self.components:
                if comp.pos == pos:
                    return comp

    def grow(self):
        """Add a new segment at the tail based on the tail's orientation."""
        tail = self.components[-1]
        tail_dir_map = {
            "NORTH": pygame.Vector2(0, 1),
            "SOUTH": pygame.Vector2(0, -1),
            "WEST": pygame.Vector2(1, 0),
            "EAST": pygame.Vector2(-1, 0)
        }

        new_pos = tail.pos + tail_dir_map[tail.orientation]

        # Add new component at calculated position
        self.add_component(new_pos, tail.orientation)

    def has_component_at(self, pos: pygame.Vector2) -> bool:
        """Return True if there is component at 'pos' coordinates"""
        for comp in self.components:
            if comp.pos == pos:
                return True
        return False

    def move(self, direction: str):
        """Snake movement with proper position and orientation updates."""
        dir_map = {
            "NORTH": pygame.Vector2(0, -1),
            "SOUTH": pygame.Vector2(0, 1),
            "WEST": pygame.Vector2(-1, 0),
            "EAST": pygame.Vector2(1, 0)
        }

        # Save current positions
        old_positions = [comp.pos.copy() for comp in self.components]
        new_head_pos = self.components[0].pos + dir_map[direction]

        # Ignore last segment when checking collision (tail moves away)
        body_positions = [comp.pos for comp in self.components[1:-1]]

        if new_head_pos in body_positions:
            self.off = True

        # Update head
        self.components[0].pos = new_head_pos
        self.components[0].orientation = direction

        # Update body segments
        for i in range(1, len(self.components)):
            self.components[i].pos = old_positions[i - 1]

            # Update orientation based on delta with previous segment
            delta = self.components[i - 1].pos - self.components[i].pos

            if delta == pygame.Vector2(0, -1):
                self.components[i].orientation = "NORTH"
            elif delta == pygame.Vector2(0, 1):
                self.components[i].orientation = "SOUTH"
            elif delta == pygame.Vector2(-1, 0):
                self.components[i].orientation = "WEST"
            elif delta == pygame.Vector2(1, 0):
                self.components[i].orientation = "EAST"

    def play_crunch(self):
        """Play crunch sound when snake eat apple"""
        self.crunch.play()

    def shrink(self):
        """Remove the last segment of the snake (the tail) if length > 1."""
        if len(self.components) > 1:
            self.components.pop()
            self.positions.pop()
            return True
        else:
            return False


class SnakeComponent:
    """SnakeComponent class"""

    def __init__(self, pos: pygame.Vector2, orientation: str):
        """SnakeComponent constructor"""
        self.pos = pos
        self.orientation = orientation


class SnakeHead(SnakeComponent):
    """SnakeHead class"""
    pass


class SnakeBody(SnakeComponent):
    """SnakeBody class"""
    pass
