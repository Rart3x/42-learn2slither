from classes.DirectionalFlags import DirectionalFlags
from classes.Snake import Snake

from dataclasses import dataclass


class Agent:
    def __init__(self, snake: Snake):
        self.alpha = 0.5    # Learning rate
        self.epsilon = 0.1  # Exploration rate
        self.gamma = 0.9    # Discount factor
        self.q_table = {}   # Q-value table
        self.score = 0.0    # Cumulative scores
        self.snake = snake  # Reference to the associated snake

        self.dangers = DirectionalFlags()
        self.foods = DirectionalFlags()


    def get_state(self):
        direction = self.snake.direction
        head = self.snake.head

    def print_bool(self):
        print("DANGER NORTH", self.dangers.north)
        print("DANGER SOUTH", self.dangers.south)
        print("DANGER WEST", self.dangers.west)
        print("DANGER EAST", self.dangers.east)

        print()

        print("FOOD NORTH :", self.foods.north)
        print("FOOD SOUTH :", self.foods.south)
        print("FOOD WEST :", self.foods.west)
        print("FOOD EAST :", self.foods.east)

    def update(self):
        self.dangers = self.snake.dangers
        self.foods = self.snake.foods
