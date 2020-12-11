import requests
import stats
import sig_check as sig
import make_trade as mkTrade
import time
from datetime import datetime
import pandas as pd

dfCol = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume", "Num_trades", "Taker_buy_base_volume", "Taker_buy_quote_volume", "Unknown"]

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
urlQuery = "?symbol=BTCUSD&interval=5m&limit=720"

#Server time call
method_time = "GET"
url_time= "https://api.binance.us"
urlPath_time = "/api/v3/time"


def get_data(begin_data):

    trueCyc =0
    fullcollection = []

    time = requests.get((url_time+urlPath_time))
    time = time.json()
    s_time = int(time['serverTime'])
    temp_time = s_time-begin_data
    while (s_time > temp_time):
        temp_url_query = urlQuery + "&startTime=" + str(temp_time)
        res = requests.get((url+urlPath+temp_url_query))
        res = res.json()
        for cs in res:
            fullcollection.append(cs)
        temp_time += 43200000
        trueCyc +=1
    dfCS = pd.DataFrame(fullcollection, columns=dfCol)
    return dfCS



def get_sma(dat, trend, pred):
    dat["Trend_sma"] = dat["Close"].rolling(trend).mean()
    dat["Pred_sma"] = dat["Close"].rolling(pred).mean()

    return dat
def get_ema(dat, trend, pred):
    dat["Trend_ema"] = dat["Trend_sma"].ewm(span=trend,adjust=False).mean()
    dat["Pred_ema"] = dat["Pred_sma"].ewm(span=pred,adjust=False).mean()

    return dat

def calc_macd(dat, trend, pred, sig):
    dat["macd"] = dat["Trend_ema"] - dat["Pred_ema"]
    dat["macd_signal"] = dat["macd"].ewm(span=trend,adjust=False).mean()

    return dat
