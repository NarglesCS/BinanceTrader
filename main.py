import requests
import stats
import sig_check as sig
import make_trade as mkTrade
import time
from datetime import datetime


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

while (len(map_ma[6]) != 1440):
    #track process time to always have information on the open interval
    start = datetime.utcnow()
    print("Cycle: " + str(len(map_ma[2])) + " True Cycle: " + str(trueCyc))

    trueCyc+=1

    #retrieve info
    res = requests.get((url+urlPath+urlQuery))
    print(res)
    print("")
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
