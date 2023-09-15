import MetaTrader5 as mt5
import pandas as pd
import sympy as sp
from mt5_lib import find_start_candle

def first_area(symbol, period, duration):
    start_idx, dataframe = find_start_candle(symbol, period, duration)
    
    planet_one, planet_two = dataframe[start_idx:start_idx+26], dataframe[start_idx+26:start_idx+52]
    
    trend = retrieve_trend(planet_one, planet_two)
    
    if trend == "UpTrend":
        L1, L2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        H1, H2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        if symbol == "XAUUSD":
            C1 = C1 / 100
            solution = solution / 100
        elif "JPY" in symbol:
            C1 = C1 / 1000
            solution = solution / 1000
        else:
            C1 = C1 / 100000
            solution = solution / 100000
            
        calibrated_pip_value_pos = C1 + solution
        calibrated_pip_value_pos = str(calibrated_pip_value_pos)
        calibrated_pip_value_pos = calibrated_pip_value_pos[:7]
        calibrated_pip_value_pos = float(calibrated_pip_value_pos)
        
        new_dataframe = dataframe[start_idx+52:]
        calibrated_candle_pos = new_dataframe[new_dataframe["close"] >= calibrated_pip_value_pos].index.tolist()[0]
        
        return calibrated_candle_pos, trend, dataframe
    
    elif trend == "DownTrend":
        L1, L2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        H1, H2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        if symbol == "XAUUSD":
            C1 = C1 / 100
            solution = solution / 100
        elif "JPY" in symbol:
            C1 = C1 / 1000
            solution = solution / 1000
        else:
            C1 = C1 / 100000
            solution = solution / 100000
            
        calibrated_pip_value_neg = C1 - solution
        calibrated_pip_value_neg = str(calibrated_pip_value_neg)
        calibrated_pip_value_neg = calibrated_pip_value_neg[:7]
        calibrated_pip_value_neg = float(calibrated_pip_value_neg)
        
        new_dataframe = dataframe[start_idx+52:]
        calibrated_candle_neg = new_dataframe[new_dataframe["close"] <= calibrated_pip_value_neg].index.tolist()[0]
        
        return calibrated_candle_neg, trend, dataframe
    
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

def second_area(symbol, period, duration):
    calibrated_candle_idx, trends, dataframe = first_area(symbol, period, duration)
    
    planet_one, planet_two = dataframe[calibrated_candle_idx-51:calibrated_candle_idx-25], dataframe[calibrated_candle_idx-25:calibrated_candle_idx+1]
    
    trend = retrieve_trend(planet_one, planet_two)
    
    if trend == "UpTrend":
        L1, L2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        H1, H2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        if symbol == "XAUUSD":
            C1 = C1 / 100
            solution = solution / 100
        elif "JPY" in symbol:
            C1 = C1 / 1000
            solution = solution / 1000
        else:
            C1 = C1 / 100000
            solution = solution / 100000
            
        return dataframe, trends, trend, L1, L2, H1, H2, C1, C2, calibrated_candle_idx, solution
    
    elif trend == "DownTrend":
        L1, L2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        H1, H2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        if symbol == "XAUUSD":
            C1 = C1 / 100
            solution = solution / 100
        elif "JPY" in symbol:
            C1 = C1 / 1000
            solution = solution / 1000
        else:
            C1 = C1 / 100000
            solution = solution / 100000
            
        return dataframe, trends, trend, L1, L2, H1, H2, C1, C2, calibrated_candle_idx, solution
    
def final_result(symbol, period, duration):
    dataframe, trends, trend, L1, L2, H1, H2, C1, C2, calibrated_candle_idx, solution = second_area(symbol, period, duration)
    
    if trend == "UpTrend":
        candle = dataframe.iloc[calibrated_candle_idx]
        low = candle["low"]

        new_period = dataframe[calibrated_candle_idx:calibrated_candle_idx+26]
        H, L = new_period["high"].max(), new_period["low"].min()
        h_idx, l_idx = new_period[new_period["high"] == H].index.tolist()[0], new_period[new_period["low"] == L].index.tolist()[0]
        
        valid_low = low
        if h_idx < l_idx:
            if H > H2:
                pass
            elif H < H2:
                if L > low:
                    pass
                elif L < low:
                    valid_low = L
        elif l_idx < h_idx:
            if L > low:
                pass
            elif L < low:
                valid_low = L
        else:
            valid_low = low
            
        valid_low = format_number(str(valid_low))
        selected_low = abs(valid_low - L1)
        
        pip_value = h_equation(L1, L2, H1, H2, C1, C2, solution, selected_low)
        
        if symbol == "XAUUSD":
            C2 = C2 / 100
            pip_value = pip_value / 100
        elif "JPY" in symbol:
            C2 = C2 / 1000
            pip_value = pip_value / 1000
        else:
            C2 = C2 / 100000
            pip_value = pip_value / 100000
            
        level = abs(C1 + pip_value)
        reach_to = abs(C2 - pip_value)
        
        return level, reach_to, trends, trend, pip_value, C1, C2, valid_low, selected_low
    
    elif trend == "DownTrend":
        candle = dataframe.iloc[calibrated_candle_idx]
        low = candle["high"]

        new_period = dataframe[calibrated_candle_idx:calibrated_candle_idx+26]
        H, L = new_period["low"].min(), new_period["high"].max()
        l_idx, h_idx = new_period[new_period["high"] == L].index.tolist()[0], new_period[new_period["low"] == H].index.tolist()[0]
        
        valid_low = low
        if h_idx < l_idx:
            if H > H2:
                if L > low:
                    pass
                elif L < low:
                    valid_low = L
            elif H < H2:
                pass
        elif l_idx < h_idx:
            if L > low:
                pass
            elif L < low:
                valid_low = L
        else:
            valid_low = low
            
        valid_low = format_number(str(valid_low))
        selected_low = abs(valid_low - L1)
        
        pip_value = h_equation(L1, L2, H1, H2, C1, C2, solution, selected_low)
        
        if symbol == "XAUUSD":
            C2 = C2 / 100
            pip_value = pip_value / 100
        elif "JPY" in symbol:
            C2 = C2 / 1000
            pip_value = pip_value / 1000
        else:
            C2 = C2 / 100000
            pip_value = pip_value / 100000
            
        level = abs(C1 - pip_value)
        reach_to = abs(C2 + pip_value)
        
        return level, reach_to, trends, trend, pip_value, C1, C2, valid_low, selected_low
    
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
    L1, L2, H1, H2, C1, C2, solution, selected_low = args
    
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
