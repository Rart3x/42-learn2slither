import pygame

from imports import paths

def load_textures(
        cell_width: int,
        cell_height: int
) -> dict[str, pygame.Surface]:
    """
    Load and return a dictionary of textures scaled to cell size.

    :param cell_width: width of the cell
    :param cell_height: height of the cell

    :return: a dictionary of textures scaled to cell size
    """
    textures = {}

    for key, path in paths.items():
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (cell_width, cell_height))
        textures[key] = img

    return textures
