import argparse
import pygame

from imports import HEIGHT, TITLE, WIDTH
from menu import menu


def main(sessions, board):
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((HEIGHT, WIDTH))

    menu(screen, sessions, board)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Learn2Slither with training options.")

    parser.add_argument("--board", action="store_true", help="Display the board during training.")
    parser.add_argument("--learn", type=bool, default=True, help="Enable learning during training.")
    parser.add_argument("--load", type=str, default="./models/empty_model.txt",
                help="Path to save the trained model.")
    parser.add_argument("--save", type=str, default="./models/",
                help="Path to save the trained model.")
    parser.add_argument("--sessions", type=int, default=0,
                        help="Number of training sessions for the AI model.")
    parser.add_argument("--visual", type=str, default="ON",
                    help="Visualize the training process (ON/OFF).")

    args = parser.parse_args()

    main(args.sessions, args.board)