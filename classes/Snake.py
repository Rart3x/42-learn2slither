import pygame


class Snake:
    """Snake class"""

    def __init__(self, initial_pos: pygame.Vector2, orientation:str):
        """Snake constructor"""
        self.head = SnakeHead(initial_pos, orientation)
        self.components: list[SnakeComponent] = [
            self.head
        ]
        self.positions: list[pygame.Vector2] = [initial_pos]

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

    def has_component_at(self, pos: pygame.Vector2) -> bool:
        """Return True if there is component at 'pos' coordinates"""
        for comp in self.components:
            if comp.pos == pos:
                return True
        return False

    def move(self, direction: str):
        """Snake movements method"""
        head = self.components[0]
        dir_map = {
            "NORTH": pygame.Vector2(0, -1),
            "SOUTH": pygame.Vector2(0, 1),
            "WEST": pygame.Vector2(-1, 0),
            "EAST": pygame.Vector2(1, 0)
        }
        new_head_pos = head.pos + dir_map[direction]

        self.positions = [new_head_pos] + self.positions[:-1]

        for i, comp in enumerate(self.components):
            comp.pos = self.positions[i]
            comp.orientation = direction if i == 0 else comp.orientation


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

