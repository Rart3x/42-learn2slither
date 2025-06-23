import pygame

GRID_COLS = 10
GRID_ROWS = 10

MOVE_DELAY = 75


def keys(key: pygame.key, player_pos: pygame.Vector2, now, last_move_time: int, running: bool) -> tuple[int, bool]:
    """Key handle function"""
    if key[pygame.K_ESCAPE]:
        running = False

    if now - last_move_time > MOVE_DELAY:

        # Up movements
        if key[pygame.K_w] or key[pygame.K_UP]:
            if player_pos.y > 0.0:
                player_pos.y -= 1

        # Down movements
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            if player_pos.y < GRID_ROWS - 1:
                player_pos.y += 1

        # Left movements
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            if player_pos.x > 0.0:
                player_pos.x -= 1

        # Right movements
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            if player_pos.x < GRID_COLS - 1:
                player_pos.x += 1

        last_move_time = now

    return last_move_time, running


def snake() -> None:
    """Snake function"""
    pygame.init()
    pygame.display.set_caption("🐍 Learn2Slither 🐍")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    CELL_WIDTH = screen.get_width() // GRID_COLS
    CELL_HEIGHT = screen.get_height() // GRID_ROWS

    random

    player_pos = pygame.Vector2(5, 5)

    last_move_time = pygame.time.get_ticks()

    while running:

        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        key = pygame.key.get_pressed()
        last_move_time, running = keys(key, player_pos, now, last_move_time, running)

        screen.fill("white")

        pygame.draw.rect(
            screen,
            "red",
            (
                player_pos.x * CELL_WIDTH,
                player_pos.y * CELL_HEIGHT,
                CELL_WIDTH,
                CELL_HEIGHT,
            ),
        )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()