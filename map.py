from imports import *
from utils import *

def create_map() -> tuple[ pygame.Vector2, list[Any], pygame.Vector2, str]:
    """Create a randomize Snake map"""
    gmap = []

    head_x = rnd.randrange(10)
    head_y = rnd.randrange(10)

    while True:
        x2 = rnd.randrange(10)
        y2 = rnd.randrange(10)

        if x2 != head_x or y2 != head_y:
            break

    for y in range(GRID_ROWS):
        row = []

        for x in range(GRID_COLS):
            row.append("0")

        gmap.append(row)

    gmap[head_y][head_x] = "H"
    gmap[y2][x2] = "A"

    gmap, snake_orientation = create_snake_body(gmap)

    print_map(gmap)

    return pygame.Vector2(x2, y2), gmap, pygame.Vector2(head_x, head_y), snake_orientation


def create_snake_body(gmap: list) -> tuple[list, str]:
    """Add snake body on gmap, choosing a valid direction randomly if multiple options are available."""
    head_y, head_x = find_snake_head(gmap)
    height = len(gmap)
    width = len(gmap[0]) if height > 0 else 0

    directions = []

    # Check NORTH (body down from head)
    if head_y + 2 < height and gmap[head_y + 1][head_x] == '0' and gmap[head_y + 2][head_x] == '0':
        directions.append(("NORTH", [(head_y + 1, head_x), (head_y + 2, head_x)]))

    # Check SOUTH (body up from head)
    if head_y - 2 >= 0 and gmap[head_y - 1][head_x] == '0' and gmap[head_y - 2][head_x] == '0':
        directions.append(("SOUTH", [(head_y - 1, head_x), (head_y - 2, head_x)]))

    # Check WEST (body right from head)
    if head_x + 2 < width and gmap[head_y][head_x + 1] == '0' and gmap[head_y][head_x + 2] == '0':
        directions.append(("WEST", [(head_y, head_x + 1), (head_y, head_x + 2)]))

    # Check EAST (body left from head)
    if head_x - 2 >= 0 and gmap[head_y][head_x - 1] == '0' and gmap[head_y][head_x - 2] == '0':
        directions.append(("EAST", [(head_y, head_x - 1), (head_y, head_x - 2)]))

    if not directions:
        # No valid direction to place the body
        return gmap, ""

    # Choose one random valid direction
    chosen_direction, body_coords = rnd.choice(directions)

    # Apply body on the map
    for y, x in body_coords:
        gmap[y][x] = 'B'

    return gmap, chosen_direction