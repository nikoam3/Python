import requests


def pedido_token(username, password):
    url = 'https://api.remarkets.primary.com.ar/auth/getToken'
    return requests.post(url, headers={"X-Username": username, "X-Password": password}).headers["X-Auth-Token"]


token = pedido_token("amayaniko5275", "rtbpuL8(")

url = "https://api.remarkets.primary.com.ar/rest/instruments/bySegment"

parameters = {"MarketSegmentID": "MERV","marketId": "ROFX"}

q = requests.get(url=url, params= parameters, headers={"X-Auth-Token": token})

q = q.json()
print(q)
