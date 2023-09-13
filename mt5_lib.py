import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz

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
    

def set_duration(duration):
    if duration == "D1":
        timeframe = mt5.TIMEFRAME_D1
    elif duration == "W1":
        timeframe = mt5.TIMEFRAME_W1
        
    return timeframe

def set_period(period):
    if period == "M1":
        timeframe = mt5.TIMEFRAME_M1
    elif period == "M5":
        timeframe = mt5.TIMEFRAME_M5
    elif period == "M15":
        timeframe = mt5.TIMEFRAME_M15
    elif period == "M30":
        timeframe = mt5.TIMEFRAME_M30
    elif period == "H1":
        timeframe = mt5.TIMEFRAME_H1
    elif period == "H2":
        timeframe = mt5.TIMEFRAME_H2
    elif period == "H4":
        timeframe = mt5.TIMEFRAME_H4

    return timeframe

def find_midline(symbol, period, duration):
    term = set_duration(duration)
    time_frame = set_period(period)
    
    candle = mt5.copy_rates_from_pos(symbol, term, 1, 1)
    dataframe = pd.DataFrame(candle)[['time', 'open', 'high', 'low', 'close']]
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s").dt.date
    
    high = dataframe["high"].values[0]
    low = dataframe["low"].values[0]
    date = dataframe["time"].values[0]
    midline = (high + low) / 2
    
    today = datetime.date.today()
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.datetime(date.year, date.month, date.day, tzinfo=timezone)
    utc_to = datetime.datetime(today.year, today.month, today.day, tzinfo=timezone)
    
    if term == mt5.TIMEFRAME_D1:
        candles = mt5.copy_rates_range(symbol, time_frame, utc_from, utc_to)
        dataframe = pd.DataFrame(candles)[['time', 'open', 'high', 'low', 'close']]
        dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s")
        
    elif term == mt5.TIMEFRAME_W1:
        target_day = 5
        days_until_target = (target_day - utc_from.weekday()) % 7
        next_target_date = utc_from + datetime.timedelta(days=days_until_target)
        
        candles = mt5.copy_rates_range(symbol, time_frame, utc_from, next_target_date)
        dataframe = pd.DataFrame(candles)[['time', 'open', 'high', 'low', 'close']]
        dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s")
        
    # start_candle1 = dataframe[dataframe['close'] >= midline]['close'].values.tolist()
    # start_candle2 = dataframe[dataframe['close'] <= midline]['close'].values.tolist()

    # diff1 = []
    # for i in start_candle1:
    #     result = i - midline
    #     diff1.append(result)
        
    # diff2 = []
    # for i in start_candle2:
    #     result = midline - i
    #     diff2.append(result)
        
    # near1 = min(diff1)
    # near2 = min(diff2)

    # real_value1 = diff1.index(near1)
    # real_value2 = diff2.index(near2)

    # real_price1 = start_candle1[real_value1]
    # real_price2 = start_candle2[real_value2]

    # candle1 = dataframe[dataframe['close'] == real_price1].index.tolist()[0]
    # candle2 = dataframe[dataframe['close'] == real_price2].index.tolist()[0]

    # if candle1 < candle2:
    #     start_point = candle1
    # elif candle2 < candle1:
    #     start_point = candle2
    # else:
    #     start_point = candle1
        
    # point = dataframe.iloc[start_point]
    # price = point['close']
    # price = round(price, 5)
    # time = point['time']
    
    start_candle = dataframe[dataframe['close'] == midline]
    if start_candle.empty:
        start_candle1 = dataframe[dataframe['close'] >= midline].index.tolist()[0]
        start_candle2 = dataframe[dataframe['close'] <= midline].index.tolist()[0]
        
        if start_candle1 < start_candle2:
            start_point = start_candle1
        elif start_candle2 < start_candle1:
            start_point = start_candle2

        point = dataframe.iloc[start_point]
        time = point['time']
    else:
        start_candle = start_candle.index.tolist()[0]
        point = dataframe.iloc[start_candle]
        time = point["time"]
        
    return time

def find_start_candle(symbol, period, duration):
    time = find_midline(symbol, period, duration)
    time_frame = set_period(period)
    
    dataframe = mt5.copy_rates_from_pos(symbol, time_frame, 1, 50000)
    dataframe = pd.DataFrame(dataframe)[['time', 'open', 'high', 'low', 'close']]
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s")
    
    start_box = dataframe[dataframe['time'] == time]
    start_idx = start_box.index.tolist()[0]
    
    return start_idx, dataframe
