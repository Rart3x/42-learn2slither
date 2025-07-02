import argparse
import pygame

from imports import HEIGHT, TITLE, WIDTH
from menu import menu


def main(sessions):
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((HEIGHT, WIDTH))

    menu(screen, sessions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Learn2Slither with training options.")
    parser.add_argument("--sessions", type=int, default=0,
                        help="Number of training sessions for the AI model.")
    args = parser.parse_args()

    main(args.sessions)