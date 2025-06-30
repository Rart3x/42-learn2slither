import pygame


def load_textures(
        cell_width: int,
        cell_height: int
) -> dict[str, pygame.Surface]:
    """
    Load and return a dictionary of textures scaled to cell size.
    """
    paths = {
        "BODY_TOP_LEFT": "assets/snake/body_top_left.png",
        "BODY_TOP_RIGHT": "assets/snake/body_top_right.png",
        "BODY_BOT_LEFT": "assets/snake/body_bot_left.png",
        "BODY_BOT_RIGHT": "assets/snake/body_bot_right.png",
        "BODY_HORIZONTAL": "assets/snake/body_horizontal.png",
        "BODY_VERTICAL": "assets/snake/body_vertical.png",
        "SNAKE_HEAD_UP": "assets/snake/head_up.png",
        "SNAKE_HEAD_DOWN": "assets/snake/head_down.png",
        "SNAKE_HEAD_LEFT": "assets/snake/head_left.png",
        "SNAKE_HEAD_RIGHT": "assets/snake/head_right.png",
        "TAIL_HEAD_UP": "assets/snake/tail_up.png",
        "TAIL_HEAD_DOWN": "assets/snake/tail_down.png",
        "TAIL_HEAD_LEFT": "assets/snake/tail_left.png",
        "TAIL_HEAD_RIGHT": "assets/snake/tail_right.png",
        "APPLE": "assets/components/apple.png",
        "MALUS": "assets/components/malus.png",
    }

    textures = {}

    for key, path in paths.items():
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (cell_width, cell_height))
        textures[key] = img

    return textures
