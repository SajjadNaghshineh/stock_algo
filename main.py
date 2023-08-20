import MetaTrader5 as mt5
from pprint import pprint
import pandas_ta as ta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import yfinance as yf
from scipy.signal import argrelextrema
from collections import deque

mt5.initialize(
    path="C:/Program Files/MetaTrader 5/terminal64.exe",
    login=51789900,
    password='s6dexjml',
    server="Alpari-MT5-Demo"
)

mt5.login(
    login=51789900,
    password='s6dexjml',
    server="Alpari-MT5-Demo"
)

candles = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M15, 0, 300)
dataframe = pd.DataFrame(candles)
dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
# print(dataframe)

def getHigherHighs(data: np.array, order=5, K=2):
    # Get highs
    high_idx = argrelextrema(data, np.greater, order=5)[0]
    highs = data[high_idx]
    # Ensure consecutive highs are higher than previous highs
    extrema = []
    ex_deque = deque(maxlen=K)
    for i, idx in enumerate(high_idx):
        if i == 0:
            ex_deque.append(idx)
            continue
        if highs[i] < highs[i-1]:
            ex_deque.clear()
            
        ex_deque.append(idx)
        if len(ex_deque) == K:
            extrema.append(ex_deque.copy())
            
    return extrema

high = dataframe['high'].values
dates = dataframe.index
order = 5
K = 2
hh = getHigherHighs(high, order, K)

hh_list = []
for high_indices in hh:
    high_values = high[high_indices]
    print(high_values)
    for j in high_values:
        hh_list.append(j)
        
highest_high = max(hh_list)

first_hh_candle = 0
second_hh_candle = 0
for high_indices in hh:
    high_values = high[high_indices]
    if highest_high in high_values:
        first_hh_candle = high_values[0]
        second_hh_candle = high_values[1]
        print(f"highest high is: {high_values}")
        print(first_hh_candle)
        print(second_hh_candle)
        
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.figure(figsize=(15, 8))
plt.plot(dataframe['high'])
_ = [plt.plot(dates[i], high[i], c=colors[1]) for i in hh]
_ = [plt.scatter(dates[i[-1]], high[i[-1]], 
    c=colors[1], marker='^', s=100) for i in hh]
plt.xlabel('Candle')
plt.ylabel('Price ($)')
plt.title(f'Potential Divergence Points for EURUSD Shadow Price')
legend_elements = [
  Line2D([0], [0], color=colors[0], label='high'),
  Line2D([0], [0], color=colors[1], label='Higher Highs'),
  Line2D([0], [0], color='w',  marker='^',
         markersize=10,
         markerfacecolor=colors[1],
         label='Higher High Confirmation')
]
plt.legend(handles=legend_elements)
plt.show()

first_hh_candle = dataframe[dataframe['high'] == first_hh_candle]
print(first_hh_candle)
second_hh_candle = dataframe[dataframe['high'] == second_hh_candle]
print(second_hh_candle)

first_time = first_hh_candle['time'].values[0]
print(first_time)
second_time = second_hh_candle['time'].values[0]
print(second_time)

first_index = first_hh_candle.index.tolist()[0]
print(first_index)
second_index = second_hh_candle.index.tolist()[0]
print(second_index)

df_after_hh = dataframe.iloc[second_index+1:]
if len(df_after_hh) > 60:
    print(df_after_hh)
else:
    print("Not enough candles!")
    
mt5.shutdown()
