import pygame

from classes.DirectionalFlags import DirectionalFlags


class Snake:
    """Snake class"""

    def __init__(self, initial_pos: pygame.Vector2, orientation="NORTH"):
        """Snake constructor"""
        self.board = False
        self.head = SnakeHead(initial_pos, orientation)

        self.components: list[SnakeComponent] = [
            self.head
        ]
        self.crunch = pygame.mixer.Sound('./assets/sounds/crunch.wav')
        self.dangers = DirectionalFlags()
        self.direction = orientation
        self.foods = DirectionalFlags()
        self.off = False
        self.positions: list[pygame.Vector2] = [initial_pos]
        self.score = 0
        self.vision = []

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

    def move(self, direction: str, gmap: list) -> bool:
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
            return False

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

        self.direction = direction
        self.view(gmap)
        
        if self.board:
            self.print_view()

        self.update_views()

        return True

    def play_crunch(self):
        """Play crunch sound when snake eat apple"""
        self.crunch.play()

    def print_view(self):
        """Print the snake's vision in the form of a cross: horizontal + vertical lines with head at the center."""
        line_view, column_view = self.vision
        width = len(line_view)
        height = len(column_view)

        head_x = line_view.index('H')
        head_y = column_view.index('H')

        for y in range(height):
            row = []
            for x in range(width):
                if x == head_x and y == head_y:
                    row.append('H')
                elif y == head_y:
                    row.append(line_view[x])
                elif x == head_x:
                    row.append(column_view[y])
                else:
                    row.append(' ')
            print("".join(row))

    def reward(self, points: int):
        """Increase the snake's score by the given points."""
        self.score = points

    def shrink(self):
        """Remove the last segment of the snake (the tail) if length > 1."""
        if len(self.components) - 1 > 1:
            self.components.pop()
            self.positions.pop()
            return True
        else:
            return False

    def update_views(self):
        """Update the bool views of the snake's vision."""
        dangers = ['W', 'S', 'R']
        foods = ['G']

        head_x, head_y = self.head.pos
        head_x, head_y = int(head_x) + 1, int(head_y) + 1

        # Update left booleans for dangers and foods
        for i in range(0, head_x):
            if self.vision[0][i] in dangers:
                self.dangers.west = True
            if self.vision[0][i] in foods:
                self.foods.west = True

        # Update up booleans for dangers and foods
        for i in range(0, head_y):
            if self.vision[1][i] in dangers:
                self.dangers.north = True
            if self.vision[1][i] in foods:
                self.foods.north = True

        # Update right booleans for dangers and foods
        for i in range(head_x, len(self.vision[0])):
            if self.vision[0][i] in dangers:
                self.dangers.east = True
            if self.vision[0][i] in foods:
                self.foods.east = True

        # Update down booleans for dangers and foods
        for i in range(head_x, len(self.vision[1])):
            if self.vision[1][i] in dangers:
                self.dangers.south = True
            if self.vision[1][i] in foods:
                self.foods.south = True

    def view(self, gmap: list[str]):
        """Store what the snake sees: all elements in its row and column, with markers for walls, head, and body."""
        head_x = int(self.head.pos.x)
        head_y = int(self.head.pos.y)

        rows = len(gmap)
        cols = len(gmap[0])

        column_view = []
        line_view = []

        if not (0 <= head_y < rows and 0 <= head_x < cols):
            self.vision = [['?'], ['?']]
            return

        body_positions = {(int(comp.pos.x), int(comp.pos.y)) for comp in self.components if comp is not self.head}

        for x in range(cols):
            if x == head_x:
                line_view.append('H')
            elif (x, head_y) in body_positions:
                line_view.append('S')
            else:
                line_view.append(gmap[head_y][x])
        line_view = ['W'] + line_view + ['W']

        for y in range(rows):
            if y == head_y:
                column_view.append('H')
            elif (head_x, y) in body_positions:
                column_view.append('S')
            else:
                column_view.append(gmap[y][head_x])
        column_view = ['W'] + column_view + ['W']

        self.vision = [line_view, column_view]


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
