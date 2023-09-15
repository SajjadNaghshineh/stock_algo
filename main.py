import mt5_lib
import settings
from strategy import second_area

mt5_lib.run_server(settings.username, settings.password, settings.server, settings.path)

t = ["M1", "M3", "M5"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["D1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(second_area(z, j, i))
            except:
                continue
            
            
t = ["M15", "M30", "H1", "H2"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["W1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(second_area(z, j, i))
            except:
                continue
            
t = ["H4"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["MN1"]

for i in d:
    for j in t:
        for z in s:
            try:
                print(f"{z}, {j}, {i}: ---------------------------------------")
                print(second_area(z, j, i))
            except:
                continue
            