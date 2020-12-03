import requests
import time
import hashlib
import hmac
import base64

def getClientKeys():
    api = open("apiKey.txt", "r")
    client = api.readline()
    client_secret = api.readline()
    api.close()
    return client[:-1], client_secret[:-1]

def getEpoch():
    return str(int(time.time()))
def genString(epoch = getEpoch(), method="", url="", body=""):
    if body =="":
        return str(epoch)+str(method)+str(url)
    else:
        return str(epoch)+method+url+str(body)
def genHash(sig, client_secret):
    return hmac.new(bytes(client_secret, 'ascii'), bytes(sig, 'ascii'), hashlib.sha256).hexdigest()

def genAuthentication(url, method, body):

    client, client_secret = getClientKeys()
    epoch = getEpoch()



    hash = genString(epoch, method, url, body)

    head = {
        "CB-VERSION" : '2020-11-19',
        "CB-ACCESS-KEY" : client,
        "CB-ACCESS-SIGN": genHash(hash,client_secret),
        "CB-ACCESS-TIMESTAMP": epoch
    }
    # req = {
    #     "grant_type": "client_credentials"
    # }
    #
    # auth_token = requests.post(url, headers = head, data = req)
    # auth_token = auth_token.json()
    # auth_head = {
    #     "Authorization" : "Bearer " +auth_token["access_token"]
    # }
    return head
