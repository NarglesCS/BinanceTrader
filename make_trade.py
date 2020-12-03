import requests

#Current price call
method_price = "GET"
url_price = "https://api.binance.us"
urlPath_price = "/api/v3/ticker/price"
urlQuery_price = "?symbol=BTCUSD"




def buy():
    res = requests.get((url_price+urlPath_price+urlQuery_price))
    res = res.json()
    price = float(res["price"])
    return True, price
def sell():
    res = requests.get((url_price+urlPath_price+urlQuery_price))
    res = res.json()
    price = float(res["price"])
    return False, price
