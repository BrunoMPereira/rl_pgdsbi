import numpy as np
import pandas as pd
import itertools

def get_stock_data(companies):
    output = pd.DataFrame(columns=['Date'])
    is_first = True
    for company in companies:
        df = pd.read_csv(f'data/{company}.csv')
        df = df[['Date', 'Close', 'Volume']]
        df = df.rename(columns={'Close': f'{company}_Close', 'Volume': f'{company}_Volume'})
        if is_first:
            output = df.copy()
            is_first = False
        else:
            output = output.merge(df, on='Date')
    output = output.drop(columns=['Date'])
    return output.values


class market_close_vol:
    def __init__(self, companies, budget=1e4):
        self.data = get_stock_data(companies)
        self.budget = budget
        self.total_days = self.data.shape[0]
        self.total_companies = len(companies)
        self.index_actions = np.arange(self.total_companies**3)
        self.action_list = list(map(list, itertools.product([0, 1, 2], repeat=self.total_companies)))

        # State: [holdings | close | volume | cash]
        self.state_size = self.total_companies * 3 + 1
        self.start()

    def get_episode_value(self):
        return self._get_eval()

    def start(self):
        self.today = 0
        self.stocks = np.zeros(self.total_companies)
        self.day_data = self.data[self.today]
        self.money_available = self.budget
        return self._get_state()

    def new_day(self, action):
        previous_val = self._get_eval()
        self.today += 1
        self.day_data = self.data[self.today] 
        self._exchange(action)
        current_val = self._get_eval()
        reward = current_val - previous_val
        done = self.today == (self.total_days - 1)
        return self._get_state(), reward, done

    def _exchange(self, action):
        actions = self.action_list[action]
        sell_list, buy_list = [], []

        for i, a in enumerate(actions):
            if a == 0:
                sell_list.append(i)
            elif a == 2:
                buy_list.append(i)

        close_prices = self.day_data[:self.total_companies]

        if sell_list:
            for i in sell_list:
                self.money_available += close_prices[i] * self.stocks[i]
                self.stocks[i] = 0

        if buy_list:
            broke = False
            while not broke:
                for i in buy_list:
                    if self.money_available > close_prices[i]:
                        self.money_available -= close_prices[i]
                        self.stocks[i] += 1
                    else:
                        broke = True

    def _get_eval(self):
        close_prices = self.day_data[:self.total_companies]
        return self.stocks.dot(close_prices) + self.money_available

    def _get_state(self):
        state = np.zeros(self.state_size)
        n = self.total_companies
        state[0:n] = self.stocks
        state[n:2*n] = self.day_data[0:n]          # Close
        state[2*n:3*n] = self.day_data[n:2*n]      # Volume
        state[-1] = self.money_available
        return state
