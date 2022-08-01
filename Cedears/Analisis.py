# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 18:42:52 2021

@author: Niko
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import requests
#import json
#import matplotlib.pyplot as plt
#import finnhub
from datetime import datetime as dt, timedelta as delta
import datetime as dt
token = "c4g1o3iad3iaqu9po5o0"

def get_History(symbol, resolution, fromDate, toDate):

    #necesitamos pasar timestamp a strings YYYY-MM-DD
    fromDT = dt.datetime.strptime(fromDate, '%Y-%m-%d')
    fromTS = int(dt.datetime.timestamp(fromDT))
    toDT = dt.datetime.strptime(toDate, '%Y-%m-%d')
    toTS = int(dt.datetime.timestamp(toDT))

    url = 'https://finnhub.io/api/v1/stock/candle'
    params = {'token': token, 'symbol': symbol, 'resolution': resolution,
              'from': fromTS, 'to': toTS}
    r = requests.get(url, params=params)
    js = r.json()
    df = pd.DataFrame(js)
    df['date'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('date', inplace=True)
    df['pct_change'] = df['c'].pct_change()*100
    df.drop(['s', 't', 'c', 'h', 'l', 'o', 'v'], axis=1, inplace=True)
    return df

tickers = ['ARKK','DIA','EEM', 'EWZ','IWM','QQQ','SPY','XLE','XLF']
tabla = []
for ticker in tickers:
    data = get_History(str(ticker), 'D', '2021-01-01', '2022-01-27')
    tabla.append(data['pct_change'])
    tabla_final = pd.concat(tabla, axis=1)
tabla_final.columns = tickers

#sirve para saber que caida de un activo tiene menos del "x%" de probabilidad que suceda
print(tabla_final.quantile(0.01))

print(tabla_final.std(), tabla_final.mean())

rendimientos = tabla_final.mean()
desvios = tabla_final.std()
tasa_libre_riesgo = (35/100) / 360

tabla_ratios = pd.DataFrame()
tabla_ratios['Quantile'] = tabla_final.quantile(0.01)
tabla_ratios['Sharpe Diario'] = (rendimientos - tasa_libre_riesgo)/desvios
tabla_ratios['Sharpe'] = tabla_ratios['Sharpe Diario']*250**0.5 #raiz cuadrada de 250
print(tabla_ratios)

sortinos = []
for activo in tickers: #ojo con la "s"
    filtro = tabla_final[activo].loc[tabla_final[activo] < 0]
    desvio_neg = filtro.std()
    sortinos.append((rendimientos[activo] - tasa_libre_riesgo) / desvio_neg)

tabla_ratios['Sortino Diario'] = sortinos
tabla_ratios['Sortino Anualizado'] = tabla_ratios['Sortino Diario'] *250**0.5 #raiz cuadrada de 250

print(tabla_ratios)

#tabla_ratios.to_excel('Cedears_Final_2020.xlsx')
