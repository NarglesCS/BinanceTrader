import requests
import pandas as pd

method = "GET"
url = "https://api.binance.us"

def getHead():
    api = open("apiKey.txt", "r")
    client = api.readline()
    client_secret = api.readline()
    api.close()
    head = {
        "X-MBX-APIKEY" : client[:-1],
    }
    return head

def getSig(params):
    pass

#Ping the api as a test for if the wrapper is working still
#Return an empty json object
def ping():
    urlPath = "/api/v3/ping"
    res = requests.get(url+urlPath)
    res = res.json()
    return res

#Return the server time as type int
def sv_time():
    urlPath = "/api/v3/time"
    res = requests.get(url+urlPath)
    res = res.json()
    return res['serverTime']

#Return a Dict of the exchanges Information
#Rate Limits
#Exchange Filters
#User Filters
def ex_info():
    urlPath = "/api/v3/exchangeInfo"
    res = requests.get(url+urlPath)
    res = res.json()
    return res

#API endpoint for the order book of depth n
#inputs are the ticker symbol and n number of records to pull
#defaults are symbol="BTCUSD" and limit=100
#returns lastUpdateId, dataframe of bids of depth n, dataframe of asks of depth n
def order_book(symbol="BTCUSD", limit=100):
    dfCol = ["price", "quantity"]
    urlPath = "/api/v3/depth"
    urlQuery = "?symbol=" + symbol + "&limit=" + str(limit)
    res = requests.get(url+urlPath+urlQuery)
    res = res.json()
    df_bids = pd.DataFrame(res['bids'], columns=dfCol)
    df_asks = pd.DataFrame(res['asks'], columns=dfCol)
    df_bids = df_bids.astype('float')
    df_asks = df_asks.astype('float')
    df_bids["total_price"] = df_bids["price"]*df_bids["quantity"]
    df_asks["total_price"] = df_asks["price"]*df_asks["quantity"]
    return  res["lastUpdateId"] , df_bids, df_asks


#API call endpoint for the recent n trades
#inputs are the ticker symbol and n number of records to pull
#defaults are symbol="BTCUSD" and limit=500
#return a dataframe of n recent trades
def rec_trades(symbol="BTCUSD", limit=500):
    urlPath = "/api/v3/trades"
    urlQuery = "?symbol=" + symbol + "&limit=" + str(limit)
    res = requests.get(url+urlPath+urlQuery)
    res = res.json()
    df_trades = pd.DataFrame(res)
    return df_trades

#API call endpoint for the n trades after a specific ID
#Request of type MARKET_DATA and requires api key
#inputs are the ticker symbol, n number of records to pull, and the ID to start from
#defaults are symbol="BTCUSD", limit=500, fromID = -1 (defaults, logic to handle non mandatory param)
#return a dataframe of n historical trades
def hist_trades(symbol="BTCUSD", limit=500, ID= -1):
    urlPath = "/api/v3/historicalTrades"
    if (ID >= 0):
        urlQuery = "?symbol=" + symbol + "&limit=" + str(limit) + "&fromId=" +str(0)
    else:
        urlQuery = "?symbol=" + symbol + "&limit=" + str(limit)
    res = requests.get(url+urlPath+urlQuery, headers=getHead())
    res = res.json()

    df_trades = pd.DataFrame(res)
    return df_trades


#API call endpoint for the n recent compressed, aggregate trades
#inputs are the ticker symbol, ID to start from, startTime in ms, endTime in ms, and n number of records to pull
#defaults are symbol="BTCUSD", ID= -1, startTime= -1, endTime = -1, and limit=500
#All defaults with negative -1 are optional and have logic to handle it
#return a dataframe of n compressed, aggregate trades from either recent or specific time
def agg_trades(symbol="BTCUSD", limit=500, startTime= -1, endTime = -1, ID= -1):
    urlPath = "/api/v3/aggTrades"
    if (startTime >=0) & (endTime < (startTime+3600000)) & (ID >=0):
        urlQuery = "?symbol=" + symbol + "&formID" + str(ID) + "&startTime=" + str(startTime) + "&endTime=" + str(endTime) + "&limit=" + str(limit)
    elif (startTime >=0) & (endTime < (startTime+3600000)):
        urlQuery = "?symbol=" + symbol + "&startTime=" + str(startTime) + "&endTime=" + str(endTime) + "&limit=" + str(limit)
    else:
        urlQuery = "?symbol=" + symbol + "&limit=" + str(limit)
    res = requests.get(url+urlPath+urlQuery)
    res = res.json()
    df_trades = pd.DataFrame(res)
    return df_trades
