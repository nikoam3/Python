import requests


def pedido_token(username, password):
    url = 'https://api.remarkets.primary.com.ar/auth/getToken'
    return requests.post(url, headers={"X-Username": username, "X-Password": password}).headers["X-Auth-Token"]


token = pedido_token("amayaniko5275", "rtbpuL8(")

url = "https://api.remarkets.primary.com.ar/rest/segment/all"

q = requests.get(url= url, headers= {"X-Auth-Token": token})

q = q.json()
print(q)

"""
DDF (Instrumentos de la División Derivados Financieros)
 DDA (Instrumentos de la División Derivados Agropecuarios)
 DUAL (Instrumentos listados en ambas divisiones)
 XVTEST (Instrumentos para realizar pruebas en producción)
 MERV (Ruteo de ordenes a la rueda de concurrencia de ofertas del Mercado de Valores de Buen os Aires S.A)
 MATBA (Ruteo de ordenes a la rueda del Mercado a Termino de Buenos Aires )
"""