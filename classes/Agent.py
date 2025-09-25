from classes.Snake import Snake


class Agent:
    def __init__(self, snake: Snake):
        self.alpha = 0.5    # Learning rate
        self.epsilon = 0.1  # Exploration rate
        self.gamma = 0.9    # Discount factor
        self.q_table = {}   # Q-value table
        self.score = 0.0    # Cumulative scores
        self.snake = snake  # Reference to the associated snake