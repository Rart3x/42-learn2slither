from imports import *

def keys(key: pygame.key, player_pos: pygame.Vector2, now, last_move_time: int, running: bool, snake_orientation: str) -> tuple[int, bool, str]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player_pos.y > 0.0:
                player_pos.y -= 1
                snake_orientation = "NORTH"

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if player_pos.y < GRID_ROWS - 1:
                player_pos.y += 1
                snake_orientation = "SOUTH"

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if player_pos.x > 0.0:
                player_pos.x -= 1
                snake_orientation = "WEST"

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player_pos.x < GRID_COLS - 1:
                player_pos.x += 1
                snake_orientation = "EAST"

        last_move_time = now

    return last_move_time, running, snake_orientation