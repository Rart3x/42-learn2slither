import pygame

from imports import HEIGHT, TITLE, WIDTH
from menu import menu


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((HEIGHT, WIDTH))

    menu(screen)


if __name__ == "__main__":
    main()
