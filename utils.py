import MetaTrader5 as mt5
import pandas as pd
import sympy as sp
import datetime
import pytz

def set_duration(duration):
    if duration == "D1":
        timeframe = mt5.TIMEFRAME_D1
    elif duration == "W1":
        timeframe = mt5.TIMEFRAME_W1
    elif duration == "MN1":
        timeframe = mt5.TIMEFRAME_MN1
        
    return timeframe

def set_period(period):
    if period == "M1":
        timeframe = mt5.TIMEFRAME_M1
    elif period == "M3":
        timeframe = mt5.TIMEFRAME_M3
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

def change_number(symbol, x, y, action):
    if action == "div":
        if symbol == "XAUUSD":
            x = x / 100
            y = y / 100
        elif "JPY" in symbol:
            x = x / 1000
            y = y / 1000
        else:
            x = x / 100000
            y = y / 100000
            
    elif action == "mul":
        if symbol == "XAUUSD":
            x = format_number(str(x))
            y = format_number(str(y))
        elif "JPY" in symbol:
            x = format_number(str(x))
            y = format_number(str(y))
        else:
            x = format_number(str(x))
            y = format_number(str(y))
            
    return x, y

def retrieve_trend(p1, p2):
    realL1, realL2 = p1["low"].min(), p2["low"].min()
    realH1, realH2 = p1["high"].max(), p2["high"].max()
    
    if realH2 > realH1 and realL2 < realL1:
        H_idx = p2[p2["high"] == realH2].index.tolist()[0]
        L_idx = p2[p2["low"] == realL2].index.tolist()[0]
        
        if H_idx > L_idx:
            trend = "UpTrend"
        elif L_idx > H_idx:
            trend = "DownTrend"
            
    elif realH2 > realH1 or realL2 > realL1:
        trend = "UpTrend"
    elif realH2 < realH1 or realL2 < realL1:
        trend = "DownTrend"
        
    return trend

def x_equation(*args):
    L1, L2, H1, H2, C1, C2 = args
    
    x = sp.symbols("x")

    diff_HL_1, diff_HL_2 = abs(H1 - L1), abs(H2 - L2)

    deltaC, deltaH, deltaL = abs(C2 - C1), abs(H2 - H1), abs(L2 - L1)

    sum_deltaC_deltaL, diff_deltaH_deltaL = abs(deltaC + deltaL), abs(deltaH - deltaL)

    equation = sp.Eq(x / diff_HL_1, ((x * diff_deltaH_deltaL) / (diff_HL_2 * diff_deltaH_deltaL)) + (((x + sum_deltaC_deltaL) * diff_HL_2) / (diff_HL_2 * diff_deltaH_deltaL)))

    solution = sp.solve(equation, x)

    solution = round(eval(str(abs(solution[0]))))
    
    return solution

def h_equation(*args):
    L1, L2, H1, H2, C1, C2, solution, selected_low, symbol = args
    
    C1, solution = change_number(symbol, C1, solution, "mul")
    
    numerator = solution - selected_low
    
    diff_HL_1, diff_HL_2 = abs(H1 - L1), abs(H2 - L2)
    deltaC, deltaH, deltaL = abs(C2 - C1), abs(H2 - H1), abs(L2 - L1)
    sum_deltaC_deltaL, diff_deltaH_deltaL = abs(deltaC + deltaL), abs(deltaH - deltaL)
    
    p1, p2, delta = solution / diff_HL_1, solution / diff_HL_2, ((solution + sum_deltaC_deltaL) /diff_deltaH_deltaL)
    values = p1 + p2 + delta
    
    x = sp.symbols("x")
    equation = sp.Eq(values * x, (numerator + (values * selected_low)))
    pip_value = sp.solve(equation, x)
    
    pip_value = round(eval(str(abs(pip_value[0]))))
    
    return pip_value

def format_number(number):
    for num in number:
        if num == ".":
            number = number.replace(num, "")
    else:
        if len(number) < 6:
            number += "0"
            number = int(number)
        elif len(number) > 6:
            number = number[:6]
            number = int(number)
        elif len(number) == 6:
            number = int(number)
            
    return number

def green_or_red(symbol, duration):
    timeframe = set_duration(duration)
    
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 1, 1)
    dataframe = pd.DataFrame(candles)
    dataframe['time'] = pd.to_datetime(dataframe['time'], unit='s').dt.date
    
    open_value = dataframe['open'].values[0]
    close_value = dataframe['close'].values[0]
    date = dataframe["time"].values[0]
    
    today = datetime.date.today()
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.datetime(date.year, date.month, date.day, tzinfo=timezone)
    utc_to = datetime.datetime(today.year, today.month, today.day, tzinfo=timezone)
    
    if timeframe == mt5.TIMEFRAME_D1:
        utc_from = utc_from
        utc_to = utc_to
        
    elif timeframe == mt5.TIMEFRAME_W1:
        target_day = 5
        days_until_target = (target_day - utc_from.weekday()) % 7
        next_target_date = utc_from + datetime.timedelta(days=days_until_target)
        
        utc_from = utc_from
        utc_to = next_target_date
        
    elif timeframe == mt5.TIMEFRAME_MN1:
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
        utc_from = utc_from
        utc_to = datetime.datetime(date.year, date.month, date2, tzinfo=timezone)
        
    if open_value < close_value:
        color = "Green"
    elif close_value < open_value:
        color = "Red"
        
    return color, utc_from, utc_to
