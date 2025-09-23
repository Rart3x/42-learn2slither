class Agent:
    def __init__(self):
        self.epsilon = 0.1  # Exploration rate
        self.alpha = 0.5    # Learning rate
        self.gamma = 0.9    # Discount factor
        self.q_table = {}   # Q-value table
        self.rate = 0.0     # Cumulative reward