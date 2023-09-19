from mt5_lib import find_start_candle
from utils import change_number, retrieve_trend, x_equation, h_equation, format_number

def first_area(symbol, period, duration):
    start_idx, dataframe = find_start_candle(symbol, period, duration)
    
    planet_one, planet_two = dataframe[start_idx:start_idx+26], dataframe[start_idx+26:start_idx+52]
    
    trend = retrieve_trend(planet_one, planet_two)
    
    if trend == "UpTrend":
        L1, L2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        H1, H2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        C1, solution = change_number(symbol, C1, solution, "div")
        
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
        
        C1, solution = change_number(symbol, C1, solution, "div")
        
        calibrated_pip_value_neg = C1 - solution
        calibrated_pip_value_neg = str(calibrated_pip_value_neg)
        calibrated_pip_value_neg = calibrated_pip_value_neg[:7]
        calibrated_pip_value_neg = float(calibrated_pip_value_neg)
        
        new_dataframe = dataframe[start_idx+52:]
        calibrated_candle_neg = new_dataframe[new_dataframe["close"] <= calibrated_pip_value_neg].index.tolist()[0]
        
        return calibrated_candle_neg, trend, dataframe
    
def second_area(symbol, period, duration):
    calibrated_candle_idx, trends, dataframe = first_area(symbol, period, duration)
    
    planet_one, planet_two = dataframe[calibrated_candle_idx-51:calibrated_candle_idx-25], dataframe[calibrated_candle_idx-25:calibrated_candle_idx+1]
    
    trend = retrieve_trend(planet_one, planet_two)
    
    if trend == "UpTrend":
        L1, L2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        H1, H2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        C1, solution = change_number(symbol, C1, solution, "div")
        
        return dataframe, trends, trend, L1, L2, H1, H2, C1, C2, calibrated_candle_idx, solution
    
    elif trend == "DownTrend":
        L1, L2 = format_number(str(planet_one["high"].max())), format_number(str(planet_two["high"].max()))
        H1, H2 = format_number(str(planet_one["low"].min())), format_number(str(planet_two["low"].min()))
        C1, C2 = format_number(str(planet_one["close"].iloc[-1])), format_number(str(planet_two["close"].iloc[-1]))
        
        solution = x_equation(L1, L2, H1, H2, C1, C2)
        
        C1, solution = change_number(symbol, C1, solution, "div")
        
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
        
        pip_value = h_equation(L1, L2, H1, H2, C1, C2, solution, selected_low, symbol)
        
        C2, pip_value = change_number(symbol, C2, pip_value, "div")
        
        level = format_number(str(abs(C1 + pip_value)))
        reach_to = format_number(str(abs(C2 - pip_value)))
        
        level, reach_to = change_number(symbol, level, reach_to, "div")
        
        return level, reach_to
    
    elif trend == "DownTrend":
        candle = dataframe.iloc[calibrated_candle_idx]
        low = candle["high"]

        new_period = dataframe[calibrated_candle_idx:calibrated_candle_idx+26]
        H, L = new_period["low"].min(), new_period["high"].max()
        l_idx, h_idx = new_period[new_period["high"] == L].index.tolist()[0], new_period[new_period["low"] == H].index.tolist()[0]
        
        valid_low = low
        if l_idx < h_idx:
            if L < low:
                pass
            elif L > low:
                valid_low = L
        elif h_idx < l_idx:
            if H < H2:
                pass
            elif H > H2:
                if L < low:
                    pass
                elif L > low:
                    valid_low = L
        else:
            valid_low = low
            
        valid_low = format_number(str(valid_low))
        selected_low = abs(valid_low - L1)
        
        pip_value = h_equation(L1, L2, H1, H2, C1, C2, solution, selected_low, symbol)
        
        C2, pip_value = change_number(symbol, C2, pip_value, "div")
        
        level = format_number(str(abs(C1 - pip_value)))
        reach_to = format_number(str(abs(C2 + pip_value)))
        
        level, reach_to = change_number(symbol, level, reach_to, "div")
        
        return level, reach_to
    