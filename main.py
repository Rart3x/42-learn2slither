import pygame
from menu import menu


def main():
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    pygame.display.set_caption("🐍 Learn2Slither 🐍")

    menu(screen)


if __name__ == "__main__":
    main()
