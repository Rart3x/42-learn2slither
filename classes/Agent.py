from classes.DirectionalFlags import DirectionalFlags
from classes.Snake import Snake

from dataclasses import dataclass
from imports import ACTIONS


class Agent:
    def __init__(self, snake: Snake):
        self.alpha = 0.5    # Learning rate
        self.epsilon = 0.1  # Exploration rate
        self.gamma = 0.9    # Discount factor
        self.q_table = {}   # Q-value table
        self.snake = snake  # Reference to the associated snake
        self.state = None

        self.previous_score = 0.0
        self.score = 0.0    # Score

        self.dangers = DirectionalFlags()
        self.foods = DirectionalFlags()

        self.q_table.setdefault(self.state, {a: 0.0 for a in ACTIONS})

    def get_reward(self):
        delta = self.snake.score - self.previous_score
        self.previous_score = self.snake.score
        return delta

    def get_state(self):
        state = (
            self.dangers.north,
            self.dangers.south,
            self.dangers.west,
            self.dangers.east,
            self.foods.north,
            self.foods.south,
            self.foods.west,
            self.foods.east,
        )
        return state

    def learn(self, state, action, reward, next_state):
        self.q_table.setdefault(state, {a: 0.0 for a in ACTIONS})
        self.q_table.setdefault(next_state, {a: 0.0 for a in ACTIONS})

        old_value = self.q_table[state][action]
        next_max = max(self.q_table[next_state].values())

        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[state][action] = new_value

    def update(self):
        self.dangers = self.snake.dangers
        self.foods = self.snake.foods
