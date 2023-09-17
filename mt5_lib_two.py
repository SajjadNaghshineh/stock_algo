import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz
from utils import green_or_red, set_period

def run_server(username, password, server, path):
    mt5.initialize(
        path=path,
        login=username,
        password=password,
        server=server
    )
    
    mt5.login(
        login=username,
        password=password,
        server=server
    )
    
def high_or_low(symbol, period, duration):
    color, utc_from, utc_to = green_or_red(symbol, duration)
    timeframe = set_period(period)
    
    candles = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    dataframe = pd.DataFrame(candles)
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
    
    if color == "Green":
        # find Low
        lowest_low = dataframe['low'].min()
        
        l_idx = dataframe[dataframe['low'] == lowest_low].index.tolist()[0]
        point = dataframe.iloc[l_idx]
        time = point['time']
        
    elif color == "Red":
        # find High
        highest_high = dataframe['high'].max()
        
        h_idx = dataframe[dataframe['high'] == highest_high].index.tolist()[0]
        point = dataframe.iloc[h_idx]
        time = point['time']
        
    return time

def find_start_candle(symbol, period, duration):
    time = high_or_low(symbol, period, duration)
    timeframe = set_period(period)
    
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 1, 50000)
    dataframe = pd.DataFrame(candles)
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s')
    
    start_candle = dataframe[dataframe['time'] == time].index.tolist()[0]
    
    return start_candle, dataframe
