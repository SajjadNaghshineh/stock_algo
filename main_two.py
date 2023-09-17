from mt5_lib_two import run_server
import settings
from strategy_two import final_result

run_server(settings.username, settings.password, settings.server, settings.path)

t = ["M1", "M3", "M5"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["D1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(final_result(z, j, i))
            except:
                continue
            
t = ["M15", "M30"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["W1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(final_result(z, j, i))
            except:
                continue
            
t = ["H1", "H2", "H4"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["MN1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(final_result(z, j, i))
            except:
                continue
            