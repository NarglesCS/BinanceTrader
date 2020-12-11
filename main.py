import requests
import stats
import sig_check as sig
import make_trade as mkTrade
import time
from datetime import datetime
import back_test as bk
import pandas as pd

mode = "back"

#ls_ma_interval = [2,4,6,12,24,48,336,1344]
ls_ma_interval = [2,4,6,18,24,48,336]
map_ma = {
    2:[],
    4:[],
    6:[],
    18:[],
    24:[],
    48:[],
    336:[]
}

#Candle Stick call 1m
method = "GET"
url = "https://api.binance.us"
urlPath = "/api/v3/klines"
urlQuery = "?symbol=BTCUSD&interval=1m&limit=1000"

#Candlestick call 30m
# method = "GET"
# url = "https://api.binance.us"
# urlPath = "/api/v3/klines"
# urlQuery = "?symbol=BTCUSD&interval=30m&limit=1000"



#Server time call
method_time = "GET"
url_time= "https://api.binance.us"
urlPath_time = "/api/v3/time"


#url = "https://api.coinbase.com"
#urlPath = "/v2/prices/BTC-USD/buy"
#urlQuery = "?date='2020-11-19'"
#body = ""
#head = con.genAuthentication(urlPath, method, body)

#res = requests.get((url+urlPath), headers = head)

#res1 = requests.get((url+urlPath))


buy = False
sell = False
risk = False
trueCyc = 0

profit =0.0
bought =0.0
sold =0.0

begin_data = 60*43200000

if mode == "back":
    ls_sma_sig = [8,16]
    ls_macd_sig = [8,16,13]
    data= bk.get_data(begin_data)
    data= bk.get_sma(data, ls_macd_sig[0],ls_macd_sig[1])
    data= bk.get_ema(data, ls_macd_sig[0],ls_macd_sig[1])
    data= bk.calc_macd(data, ls_macd_sig[0], ls_macd_sig[1], ls_macd_sig[2])
    for i in range(len(data)):
        if i>0:
            if (bool(float(data.iloc[i]["macd"]) >= float(data.iloc[i]["macd_signal"])) & bool(float(data.iloc[i-1]["macd"]) <= float(data.iloc[i-1]["macd_signal"])) & (not risk)):
                bought = data.iloc[i]["Close"]
                risk = True

            elif (bool(float(data.iloc[i]["macd"]) <= float(data.iloc[i]["macd_signal"])) & bool(float(data.iloc[i-1]["macd"]) >= float(data.iloc[i-1]["macd_signal"])) & (risk)):
                sold = data.iloc[i]["Close"]
                profit += (float(sold)-float(bought))
                bought = 0.0
                sold = 0.0
                risk = False
                fin_sell = data.iloc[i]["Close"]
        elif i==0:
            init_buy = data.iloc[i]["Close"]

    print("Regular strat: " + str(float(fin_sell) - float(init_buy)))
    print("Bot Strat: " + str(profit))



elif mode == "live":
    while (len(map_ma[6]) != 1440):
        #track process time to always have information on the open interval
        start = datetime.utcnow()
        print("Cycle: " + str(len(map_ma[2])) + " True Cycle: " + str(trueCyc))

        trueCyc+=1

        #retrieve info
        res = requests.get((url+urlPath+urlQuery))
        res = res.json()
        #calculate ma
        map_ma = stats.update_map(res)
        #check buy conditions
        if (trueCyc>1):
            buy = sig.ma_buy_sig(map_ma,6,18,risk)
            sell = sig.ma_sell_sig(map_ma,6,18,risk)

        if (buy)&(not risk):
            risk, bought = mkTrade.buy()
            print("Bought at: " + str(bought))

        elif (sell)&(risk):
            risk, sold = mkTrade.sell()
            print("Sold at: " + str(sold))
            print("Profit/Loss: " + str(sold-bought))
            profit += (sold-bought)
            print("Running Profit: " + str(profit))

        #check process time and sleep until the next interval release
        sleep = (60 - (start.second + start.microsecond/1000000.0))

        #every min
        time.sleep(sleep)
        #every 30 min
        # time.sleep(1800-elapsed)
