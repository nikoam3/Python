# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 18:50:37 2022

@author: Niko
"""
import time
import requests
import pandas as pd
import datetime as dt

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging


"VARIABLES A CONFIGURAR"
dias = 7

"FUNCIONES"
def prices(per, interval, from_date=None, to_date=None):
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

"LOG" 
config_logging(logging, logging.DEBUG)

key = ""
secret = ""

spot_client = Client(key, secret)
test = spot_client.coin_info()

"ARMADO DE DATOS"
tickers = [t['coin'] for t in test] #creo lista con todos las monedas
listado = {}


for i in test:
    data = pd.DataFrame() #creo y reseteo los datos
    inicio = dt.datetime.now() - dt.timedelta(days=dias) #donde comienza la toma de datos
    fecha_fin = int(dt.datetime.now().timestamp()) * 1000 #finaliza en este momento
    
    if len(prices(i['coin']+'BUSD', '5m')) > 0: #pregunto si tiene par BUSD para tradear
        while inicio < pd.to_datetime(fecha_fin, unit='ms'):
            data_temp = prices(i['coin']+'BUSD', '5m', None, fecha_fin)
            fecha_fin = int((data_temp.index[0] - dt.timedelta(minutes=5)).timestamp())*1000
            data = pd.concat([data_temp,data])
            
    listado[i['coin']] = data

    