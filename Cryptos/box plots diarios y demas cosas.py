# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 17:39:33 2022

@author: Niko
"""

import pandas as pd
import requests
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf


#import talib
#import time
#import logging
#import os
#from datetime import datetime as dt
#from binance.spot import Spot as Client
#from binance.lib.utils import config_logging
#from binance.error import ClientError


def prices(per, interval, from_date, to_date):
    url = 'https://api.binance.com/api/v3/klines'
    p = {'symbol': per, 'interval': interval, 'startTime': from_date,
         'endTime': to_date, 'limit': 1000}
    r = requests.get(url, params=p)
    js = r.json()

    col = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Volume_q',
           'cTime', 'trades', 'talerBase', 'takerQupte', 'Ignore']
    df = pd.DataFrame(js, columns=col)
    df = df.apply(pd.to_numeric)
    df.index = pd.to_datetime(df.Time, unit='ms')
    df = df.drop(['Time', 'Volume_q', 'cTime', 'trades', 'talerBase',
                  'takerQupte', 'Ignore'], axis=1)
    return df

"""
INTENTE BAJAR LOS DATOS DESDE LA API DE BINANCES PERO NO FUNCIONA CORRECTAMENTE PARA PERIODOS LARGOS
ahora = dt.datetime.now()
antes = ahora-dt.timedelta(days=500)
antes1 = ahora - dt.timedelta(days=2000)
dt.datetime.timestamp(ahora)
data = prices('BTCUSDT', '1d', int(dt.datetime.timestamp(antes)), None)
data = prices('BTCUSDT', '1d', int(dt.datetime.timestamp(last)), None)
"""

btc = yf.Ticker("BTC-USD")
data = btc.history(period="max")

data = yf.download('BTC-USD', start=str((dt.date.today())-(dt.timedelta(days=7))), interval='5m')

data_pct = pd.DataFrame()
data_pct['var'] = data.Close.pct_change()
data_pct['%'] = data.Close.pct_change()*100
#detalles = data.describe()
print(data_pct['%'].std(), data_pct['%'].mean())
print(data_pct['%'].quantile(0.01))
#esto quiere decir que una caida diaria de -xxx o peor tiene un 1% (0.01) de probabilidad que suceda

#VOLATILIDAD
volatilidad = data_pct['var'].rolling(250).std() * 100 * (250)**0.5
volatilidad.plot()


#calculos de variacones diarias
data_pct = data_pct.dropna()
#data_pct = data_pct.loc[data_pct.index > '2021-10-25']
data_x_dia = {}
for i in range(7):
    data_x_dia[i] = data_pct.loc[data_pct.index.dayofweek == i]

dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
data_day = []
for i in range(7):
    data_day.append(data_x_dia[i])

fig, ax = plt.subplots(figsize=(14, 6))
ax.boxplot(data_day, vert=True, showmeans=True, showfliers=True)
line = ax.plot([1,7], [0,0], 'k--', lw=0.5)
plt.xticks([i for i in range(1, len(dias)+1)], dias)
#ax.set_ylim([-0.15,0.2])
plt.show()
