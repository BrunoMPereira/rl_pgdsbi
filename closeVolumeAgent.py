import numpy as np

class VolumeMomentumAgent:
    def __init__(self, num_actions, num_companies):
        self.num_actions = num_actions
        self.num_companies = num_companies
        self.history = []

    def act(self, state):
        n = self.num_companies
        close_prices = state[n:2*n]
        volumes = state[2*n:3*n]

        today = list(zip(close_prices, volumes))
        self.history.append(today)

        if len(self.history) < 2:
            return np.random.choice(self.num_actions)

        actions = []
        for i in range(n):
            close_today, vol_today = self.history[-1][i]
            close_prev, vol_prev = self.history[-2][i]

            if close_today > close_prev and vol_today > vol_prev:
                actions.append(2)  # Buy
            elif close_today < close_prev and vol_today < vol_prev:
                actions.append(0)  # Sell
            else:
                actions.append(1)  # Hold

        # Convert actions list to single index
        action_index = 0
        for i, a in enumerate(actions):
            action_index += a * (3 ** (n - i - 1))

        return action_index
