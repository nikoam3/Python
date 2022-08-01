# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 11:37:28 2022

@author: Niko
"""

import requests
import pandas as pd
import datetime as dt
import telebot
import talib 
from numba import jit, njit
import dask
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging


"VARIABLES A CONFIGURAR"
token_telegram = ''
bot = telebot.TeleBot(token_telegram)
cantidad_minutos = 288 #esto equivale a 1 dias cada 5 minutos

"FUNCIONES"
def prices(per, interval, from_date=None, to_date=None):
    url = 'https://api.binance.com/api/v3/klines'
    p = {'symbol': per, 'interval': interval, 'startTime': from_date,
         'endTime': to_date, 'limit': cantidad_minutos}
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

def ticker(per):
    url = 'https://api.binance.com/api/v3/ticker'
    p = {'symbol': per, 'windowSize': '5m'}
    r = requests.get(url, params=p)
    js = r.json()
    return js


"LOG" 
config_logging(logging, logging.DEBUG)
key = ""
secret = ""

"LISTADO DE TICKERS" 
spot_client = Client(key, secret)
tickers = [t['coin'] for t in spot_client.coin_info()]

"NUMBA"
@jit
def wow_numba(data):
    #calculo la varacion en porcentaje de precio en precio
    data['%_Change'] = data['Close'].pct_change() * 100
    #media de volumen
    data['Vol_Med'] = talib.SMA(data['Volume'], timeperiod=14) 
    #condicion para que mande msj
    #if (data['%_Change'][-1] > 5) or (data['Volume'][-1] > data['Vol_Med'][-1]*10):
    if (data['%_Change'][-1] > 5):    
        bot.send_message(5497003275, str(f"Verificar {i} \n posible pump!"))


"SCREENER"
while True:
    now = dt.datetime.now()
    minutes = now.minute
    seconds = now.second

    if ((minutes == 0) | (minutes == 5) | (minutes == 10) | (minutes == 15) |
        (minutes == 20) | (minutes == 25) |(minutes == 30) | (minutes == 35) |
        (minutes == 40) | (minutes == 45) | (minutes == 50) | (minutes == 55)) & (seconds == 1):

        for i in tickers:
            try:
                #descargo los precios de los ultimos dias
                data = prices(i+'USDT', '5m')
                #pregunto si tiene par USDT para tradear
                if len(data) > 0:
                    #inicializo numba para que los procesos los realiace mas rapido
                    wow_numba(data)
            except:
                pass
