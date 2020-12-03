import coinbase_api_connector as con
import requests
import stats
import time
from datetime import datetime


#ls_ma_interval = [2,4,6,12,24,48,336,1344]
ls_ma_interval = [2,4,6,12,24,48,336]
map_ma = {
    2:[],
    4:[],
    6:[],
    12:[],
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

#Current price call
method_price = "GET"
url_price = "https://api.binance.us"
urlPath_price = "/api/v3/ticker/price"
urlQuery_price = "?symbol=BTCUSD"

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

profit =0.0
bought =0.0
sold =0.0

risk = False

trueCyc = 0

while (len(map_ma[2]) != 1440):
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
        if ((stats.get_cur_ma(map_ma[4])) >= (stats.get_cur_ma(map_ma[48]))) & ((stats.get_prev_ma(map_ma[4])) <= (stats.get_prev_ma(map_ma[48]))) & (not risk):
            resB = requests.get((url_price+urlPath_price+urlQuery_price))
            resB = resB.json()
            bought = float(resB["price"])
            print("Bought at: " + resB["price"])
            risk =True
        elif ((stats.get_cur_ma(map_ma[4])) <= (stats.get_cur_ma(map_ma[48]))) & ((stats.get_prev_ma(map_ma[4])) >= (stats.get_prev_ma(map_ma[48]))) & (risk):
            resS = requests.get((url_price+urlPath_price+urlQuery_price))
            resS = resS.json()
            sold = float(resS["price"])
            print("Sold at: " + resS["price"])
            print("Profit/Loss: " + str(sold-bought))
            risk= False
            profit += (sold-bought)
            bought=0
            sold=0
            print("Running Profit: " + str(profit))



    #check process time and sleep until the next interval release
    sleep = (60 - (start.second + start.microsecond/1000000.0))

    #every min
    time.sleep(sleep)
    #every 30 min
    # time.sleep(1800-elapsed)
