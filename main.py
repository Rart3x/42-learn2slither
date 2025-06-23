import os
import pygame


def snake():
    """Snake function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)

    pygame.quit()


def main():
    """Main function"""
    snake()


if __name__ == "__main__":
    main()