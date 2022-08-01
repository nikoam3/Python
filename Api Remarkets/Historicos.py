import requests


def pedido_token(username, password):
    url = 'https://api.remarkets.primary.com.ar/auth/getToken'
    return requests.post(url, headers={"X-Username": username, "X-Password": password}).headers["X-Auth-Token"]


token = pedido_token("amayaniko5275", "rtbpuL8(")

url = "https://api.remarkets.primary.com.ar/rest/data/getTrades?marketId=ROFX&symbol=DOEne18&date=YYYY-MM-DD"

parameters = {"marketId": "ROFX", "symbol": "MERV - XMEV - ALUA - 48hs", "dateFrom": "2020-10-04", "dateTo":  "2020-11-11"}
parameters1 = {"marketId": "ROFX", "symbol": "RFX20Dic20", "dateFrom": "2020-10-04", "dateTo": "2020-11-10"}

w = requests.get(url=url, params=parameters, headers={"X-Auth-Token": token})
e = requests.get(url=url, params=parameters1, headers={"X-Auth-Token": token})

w = w.json()
#w = w["marketData"]["CL"]["price"]
e = e.json()
#e = e["marketData"]["CL"]["price"]

print("Precio de Cierre de GGAL es: $",w,)
print("Precio de Cierre de RFX20Dic20 es: $",e)