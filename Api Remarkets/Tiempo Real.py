import requests


def pedido_token(username, password):
    url = 'https://api.remarkets.primary.com.ar/auth/getToken'
    return requests.post(url, headers={"X-Username": username, "X-Password": password}).headers["X-Auth-Token"]


token = pedido_token("amayaniko5275", "rtbpuL8(")

url = "https://api.remarkets.primary.com.ar/rest/marketdata/get"

parameters = {"marketId": "ROFX", "symbol": "MERV - XMEV - YPFD - 48hs", "entries": "CL", "depth": "5"}
parameters1 = {"marketId": "ROFX", "symbol": "RFX20Dic20", "entries": "CL", "depth": "5"}

w = requests.get(url=url, params=parameters, headers={"X-Auth-Token": token})
e = requests.get(url=url, params=parameters1, headers={"X-Auth-Token": token})

w = w.json()
w = w["marketData"]["CL"]["price"]
e = e.json()
e = e["marketData"]["CL"]["price"]

print("Precio de Cierre de YPDF es: $",w,)
print("Precio de Cierre de ALUA es: $",e)


"""""
BI: BIDS Mejor oferta de compra en el Book OF
OF: OFFERS Mejor oferta de venta en el Book LA
LA: LAST Último precio operado en el mercado OP
OP: OPENING PRICE Precio de apertura CL
CL: CLOSING PRICE Precio de cierre SE
SE: SETTLEMENT PRICE Precio de ajuste (solo para futuros) HI
HI: TRADING SESSION HIGH PRICE Precio máximo de la rueda LO
LO: TRADING SESSION LOW PRICE Precio mínimo de la rueda TV
TV: TRADE VOLUME Volumen operado en contratos/nominales para ese security OI
OI: OPEN INTEREST Interés abierto (solo para futuros) IV
IV: INDEX VALUE Valor del índice (solo para índices) EV
EV: TRADE EFFECTIVE VOLUME Volumen efectivo de negociación para ese security NV
NV: NOMINAL VOLUME Volumen nominal de negociación para ese security
"""