# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 21:36:21 2021

@author: Niko
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
token = "c4g1o3iad3iaqu9po5o0"


def get_HistoryCry(exchange, symbol, resolution, fromDate, toDate):
    symbol = exchange+ ':' +symbol

    #paso timestamp a strings YYYY-MM-DD
    fromDT = dt.datetime.strptime(fromDate, '%Y-%m-%d')
    fromTS = int(dt.datetime.timestamp(fromDT))
    toDT = dt.datetime.strptime(toDate, '%Y-%m-%d')
    toTS = int(dt.datetime.timestamp(toDT))

    url = 'https://finnhub.io/api/v1/crypto/candle'
    params = {'token': token, 'symbol': symbol, 'resolution': resolution,
              'from': fromTS, 'to': toTS}
    r = requests.get(url, params=params)
    js = r.json()
    df = pd.DataFrame(js)
    df['date'] = pd.to_datetime(df['t'], unit='s')
    df.set_index('date', inplace=True)
    df[symbol] = df['c'].pct_change()*100
    df.drop(['s', 't', 'h', 'l', 'o', 'v', 'c'], axis=1, inplace=True)
    return df

def graficar_correlacion(dfCorr, title=''):
    fig = plt.figure(figsize=(12, 8))
    plt.matshow(dfCorr, fignum=fig.number) #con esto se grafica
    plt.xticks(range(dfCorr.shape[1]), dfCorr.columns, fontsize=12, rotation=90) #shape(nos devuelve la forma de la matriz)
    plt.yticks(range(dfCorr.shape[1]), dfCorr.columns, fontsize=12)
    cb = plt.colorbar(orientation='vertical', label='Factor Correlacion 'r'')
    cb.ax.tick_params(labelsize=12)
    plt.title(title, fontsize=14, y=1.2)

    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, len(dfCorr), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(dfCorr), 1), minor=True)
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)

    for i in range(dfCorr.shape[0]):
        for j in range(dfCorr.shape[1]):
            fig.gca().text(i, j, "{:.2f}". format(dfCorr.iloc[i,j]), ha='center',
                       va='center', c='white', size=10, fontweight='bold')
    return(plt)

symbols = ['DOGEUSDT', 'SHIBUSDT']

data_corr = pd.DataFrame()
for symbol in symbols:
    data = get_HistoryCry('BINANCE', str(symbol), 'D', '2020-08-01', '2022-04-17')
    data.columns = [str(symbol)]
    data_corr = pd.concat([data_corr, data[str(symbol)]], axis=1)

#prueba para que sea mas eficiente el script
#data_corr = round(data_corr.corr(),3)
#data_corr.style.background_gradient(cmap='binary').set_precision(3)
#print(data_corr)

plt = graficar_correlacion(data_corr.corr(), 'Correlacion diaria')
plt.show()






