import requests

#Current price call
method_price = "GET"
url_price = "https://api.binance.us"
urlPath_price = "/api/v3/ticker/price"
urlQuery_price = "?symbol=BTCUSD"

profit =0.0
bought =0.0
sold =0.0


def buy():
    res = requests.get((url_price+urlPath_price+urlQuery_price))
    res = res.json()
    bought = float(res["price"])
    print("Bought at: " + resB["price"])
    return True
def sell():
    res = requests.get((url_price+urlPath_price+urlQuery_price))
    res = res.json()
    sold = float(res["price"])
    print("Sold at: " + res["price"])
    print("Profit/Loss: " + str(sold-bought))
    profit += (sold-bought)
    bought=0.0
    sold=0.0
    print("Running Profit: " + str(profit))
    return False
