import pygame

from menu import menu


def main():
    pygame.init()
    pygame.display.set_caption("🐍 Learn2Slither 🐍")

    screen = pygame.display.set_mode((750, 750))

    menu(screen)


if __name__ == "__main__":
    main()
