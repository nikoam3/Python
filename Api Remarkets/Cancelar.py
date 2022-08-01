import requests


def pedido_token(username, password):
    url = 'https://api.remarkets.primary.com.ar/auth/getToken'
    return requests.post(url, headers={"X-Username": username, "X-Password": password}).headers["X-Auth-Token"]


token = pedido_token("amayaniko5275", "rtbpuL8(")

# Emitir una orden
url = "https://api.remarkets.primary.com.ar/rest/order/newSingleOrder"

parameters = {"marketId": "ROFX", "symbol": "RFX20Dic20", "price": "69000",
              "orderQty": "5", "ordType": "Limit", "side": "Buy", "timeInForce": "Day", "account": "REM5275"}

q = requests.get(url=url, params=parameters, headers={"X-Auth-Token": token})

q = q.json()

num_orden = q["order"]["clientId"]

print("Numero de Operacion:", num_orden)

url = "https://api.remarkets.primary.com.ar/rest/order/cancelById"

parameters = {"clOrdId": num_orden, "proprietary": "PBCP"}

w = requests.get(url=url, params=parameters, headers={"X-Auth-Token": token})

w = w.json()

can_orden = w["order"]["clientId"]

print("Cancelacion orden n.:", can_orden)