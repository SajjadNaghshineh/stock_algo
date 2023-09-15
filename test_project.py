import os
os.system("cls")
import sympy as sp
import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz

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

symbol = input("Enter Symbol: ").upper()

def make_time():
    timeframe = input("Enter time frame: ").upper()
    if timeframe == "M1":
        timeframe = mt5.TIMEFRAME_M1
    elif timeframe == "M3":
        timeframe = mt5.TIMEFRAME_M3
    elif timeframe == "M5":
        timeframe = mt5.TIMEFRAME_M5
    elif timeframe == "M15":
        timeframe = mt5.TIMEFRAME_M15
    elif timeframe == "M30":
        timeframe = mt5.TIMEFRAME_M30
    elif timeframe == "H1":
        timeframe = mt5.TIMEFRAME_H1
    elif timeframe == "H2":
        timeframe = mt5.TIMEFRAME_H2
    elif timeframe == "H4":
        timeframe = mt5.TIMEFRAME_H4
    elif timeframe == "D1":
        timeframe = mt5.TIMEFRAME_D1
    elif timeframe == "W1":
        timeframe = mt5.TIMEFRAME_W1
    elif timeframe == "MN1":
        timeframe = mt5.TIMEFRAME_MN1
    return timeframe

timeframe = make_time()
candle = mt5.copy_rates_from_pos(symbol, timeframe, 1, 1)
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

if timeframe == mt5.TIMEFRAME_MN1:
    if date.month == 2:
        if date.year % 4 == 0:
            date1 = abs(date.day - 29)
        else:
            date1 = abs(date.day - 28)
            
    elif date.month in (1, 3, 5, 6, 7, 8, 10, 12):
        date1 = abs(date.day - 31)
        
    elif date.month in (4, 9, 11):
        date1 = abs(date.day - 30)
        
    date2 = date.day + date1
    utc_to = datetime.datetime(date.year, date.month, date2, tzinfo=timezone)
    
    timeframe = make_time()
    candles = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
    dataframe = pd.DataFrame(candles)[['time', 'open', 'high', 'low', 'close']]
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s")

elif timeframe == mt5.TIMEFRAME_W1:
    day_of_week = utc_from.weekday()
    target_day = 5
    days_until_target = (target_day - utc_from.weekday()) % 7
    next_target_date = utc_from + datetime.timedelta(days=days_until_target)

    timeframe = make_time()
    candles = mt5.copy_rates_range(symbol, timeframe, utc_from, next_target_date)
    dataframe = pd.DataFrame(candles)[['time', 'open', 'high', 'low', 'close']]
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit="s")

elif timeframe == mt5.TIMEFRAME_D1:
    timeframe = make_time()
    candles = mt5.copy_rates_range(symbol, timeframe, utc_from, utc_to)
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
    
if timeframe == mt5.TIMEFRAME_M1:
    df_m1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 1, 50000)
    df_m1 = pd.DataFrame(df_m1)[['time', 'open', 'high', 'low', 'close']]
    df_m1['time'] = pd.to_datetime(df_m1['time'], unit="s")
    
    start_box = df_m1[df_m1['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_M5:
    df_m5 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 1, 50000)
    df_m5 = pd.DataFrame(df_m5)[['time', 'open', 'high', 'low', 'close']]
    df_m5['time'] = pd.to_datetime(df_m5['time'], unit="s")
    
    start_box = df_m5[df_m5['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_M15:
    df_m15 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 1, 50000)
    df_m15 = pd.DataFrame(df_m15)[['time', 'open', 'high', 'low', 'close']]
    df_m15['time'] = pd.to_datetime(df_m15['time'], unit="s")
    
    start_box = df_m15[df_m15['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_M30:
    df_m30 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M30, 1, 50000)
    df_m30 = pd.DataFrame(df_m30)[['time', 'open', 'high', 'low', 'close']]
    df_m30['time'] = pd.to_datetime(df_m30['time'], unit="s")
    
    start_box = df_m30[df_m30['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_H1:
    df_h1 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 1, 50000)
    df_h1 = pd.DataFrame(df_h1)[['time', 'open', 'high', 'low', 'close']]
    df_h1['time'] = pd.to_datetime(df_h1['time'], unit="s")
    
    start_box = df_h1[df_h1['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_H2:
    df_h2 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H2, 1, 50000)
    df_h2 = pd.DataFrame(df_h2)[['time', 'open', 'high', 'low', 'close']]
    df_h2['time'] = pd.to_datetime(df_h2['time'], unit="s")
    
    start_box = df_h2[df_h2['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
elif timeframe == mt5.TIMEFRAME_H4:
    df_h4 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 1, 50000)
    df_h4 = pd.DataFrame(df_h4)[['time', 'open', 'high', 'low', 'close']]
    df_h4['time'] = pd.to_datetime(df_h4['time'], unit="s")
    
    start_box = df_h4[df_h4['time'] == time]
    if not start_box.empty:
        print(start_box)
    else:
        print("not found")
        
start_idx = start_box.index.tolist()[0]
print(start_idx)
print(time)

mt5.shutdown()
