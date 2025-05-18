import numpy as np
import pandas as pd

class RSIAgent:
    def __init__(self, num_actions, num_companies, window=3):
        self.num_actions = num_actions
        self.num_companies = num_companies
        self.window = window
        self.history = []

    def _compute_rsi(self, prices):
        prices = pd.Series(prices)
        delta = prices.diff()
        gain = (delta.clip(lower=0)).rolling(self.window).mean()
        loss = (-delta.clip(upper=0)).rolling(self.window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def act(self, state):
        prices = state[self.num_companies:2*self.num_companies]
        self.history.append(prices)

        if len(self.history) < self.window + 1:
            return np.random.choice(self.num_actions)
        
        actions = []

        for i in range(self.num_companies):
            # Gather price history for this company
            prices_history_company = [h[i] for h in self.history]
            rsi_series = self._compute_rsi(prices_history_company)

            if pd.isna(rsi_series.iloc[-1]):
                actions.append(1)  # Hold (default)
            else:
                rsi = rsi_series.iloc[-1]
                if rsi < 30:
                    actions.append(2)  # Buy
                elif rsi > 70:
                    actions.append(0)  # Sell
                else:
                    actions.append(1)  # Hold

        # Convert to index
        action_index = 0
        for i, a in enumerate(actions):
            action_index += a * (3 ** (self.num_companies - i - 1))

        return action_index
