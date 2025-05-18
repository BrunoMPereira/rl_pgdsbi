# Stock Trading with Reinforcement Learning

This project simulates a stock trading environment using historical data. You can test different types of agents that make trading decisions based on closing prices, volume, or technical indicators.
This work was done with help of ChatGPT

# Project Structure
Several python files with agents and markets.
_market_ files are related with markets.
_Agent_ termination files are related with agents.


# Agents
* RandomAgent – Takes random actions - _randomAgent.py_

* MomentumAgent – Uses a short-term momentum window - _momentumagent.py_

* MomentumAgentV2 – Reverse logic of MomentumAgent for a momentum window - _`momentumagent_v2`.py_

* RSIAgent – Uses RSI to detect overbought/oversold - _`rsi_agent`.py_

* VolumeMomentumAgent – Buys if both price and volume go up - _closeVolumeAgent.py_

# Environments
Each environment provides a different input:

* _market.py_ - Specific column only, i.e., Close or Open

* _`market_changes`.py_ - Adjusted close price percentage from Close

* _`market_close_volume`.py_ - Close + Volume within state


## The state includes:
* Stocks held
* Current price info
* Available cash

# How to Run
Add CSV files to the data/ folder with columns: Date, Close, Volume

Run the IPython notebook with all the imports and functions to visualize result
