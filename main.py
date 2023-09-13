import mt5_lib
import settings

mt5_lib.run_server(settings.username, settings.password, settings.server, settings.path)

t = ["M1", "M5", "M15"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["D1"]

for i in d:
    for j in t:
        for z in s:
            print(f"{z}, {j}, {i}: ", mt5_lib.find_start_candle(z, j, i, 1, 50000))
            
t = ["M30", "H1", "H2", "H4"]
s = ["NZDUSD", "AUDUSD", "USDJPY", "USDCAD", "USDCHF", "CADJPY", "AUDNZD", "CADCHF", "EURNZD", "EURJPY"]
d = ["W1"]

for i in d:
    for j in t:
        for z in s:
            print(f"{z}, {j}, {i}: ", mt5_lib.find_start_candle(z, j, i, 1, 50000))
            