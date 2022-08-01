# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 18:59:21 2022

@author: Niko

Muestra de funcionamiento de Bot cada 5 minutos
"""
import pandas as pd
import requests
import talib
import time
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError


#API BINANCE
key = ""
secret = ""

#inicio variables
per = 'APEUSDT' #par
symbol = 'APE' #simbolo
decimal_price = 4 #cantidad de decimales a redondear en precios
decimal_quantity = 2 #cantidad de decimales a redondear en cantidad
bot = True #trabaja o no trabaja el bot
buy = False #estado de bot, comprado
ciclos = 0
compras = 0
ventas = 0
stops_loss = 0
take_profit = 0
saldo = float(0)
price_take_profit = 0
stop_take_price = 0 
stop_price = 0
traders = [] #almaceno traders confirmados


#creo directorio donde se guardaran los registros de ordenes
try:
    location = os.getcwd()
    if location == location+'Registro '+str(per):
        pass
    else:
        os.mkdir("Registro " + str(per))
        os.chdir("Registro " + str(per))
except:
    pass


def get_order_book(per):
    url = 'https://api.binance.com/api/v3/depth'
    p = {'symbol': per, 'limit': 5}
    r = requests.get(url, params=p)
    js = r.json()
    bids = pd.DataFrame(js['bids'])
    asks = pd.DataFrame(js['asks'])
    df = pd.concat([bids[1],bids[0],asks[0], asks[1]], axis=1)
    df.columns = ['bid_quant', 'bid_price', 'ask_price', 'ask_quant']
    df = df.reindex(columns=['bid_quant', 'bid_price', 'ask_price', 'ask_quant'])
    df = df.apply(pd.to_numeric).round(decimal_price)
    return df

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

def new_order(per, side, price, quantity):
    if side == 'BUY':
        params = {"symbol": per, "side": side, "type": "LIMIT",
                      "timeInForce": "GTC", "quantity": quantity,
                      "price": price}
    else:
        params = {"symbol": per, "side": side, "type": "LIMIT",
                      "timeInForce": "GTC", "quantity": quantity,
                      "price": price}
    try:
        response = client.new_order(**params)
        logging.info(response)
    except ClientError as error:
        logging.error("Found error. status: {}, error code: {},error message: {}".format(error.status_code,
                      error.error_code, error.error_message))
    return response


while bot == True:
    #logica para que actue cada 5 min exactamente
    now = dt.datetime.now()
    minutes = now.minute
    seconds = now.second

    if ((minutes == 0) | (minutes == 5) | (minutes == 10) | (minutes == 15) |
        (minutes == 20) | (minutes == 25) |(minutes == 30) | (minutes == 35) |
        (minutes == 40) | (minutes == 45) | (minutes == 50) | (minutes == 55)) & (seconds == 1):

        """LOGIN"""
        config_logging(logging, logging.DEBUG)
        client = Client(key, secret)

        """SALDO"""
        client_account = client.account()
        saldo = float(next(x for x in client_account['balances'] if x["asset"] == "USDT")['free'])

        """PRECIO"""
        data = prices(per, '5m')
        data['Vol_Med'] = talib.MA(data.Volume, timeperiod=20)
        data['ADX'] = talib.ADX(data.High, data.Low, data.Close)
        data['SAR'] = talib.SAR(data.High, data.Low, acceleration=0.02, maximum=0.2)
        data['RSI'] = talib.RSI(data.Close, timeperiod=14)

        """COMPRAR"""
        if #estrategia de compra:
            #si mi saldo me deja, compro
            if saldo > 11:
                #ultimo precio de compra
                price = float(get_order_book(per)['bid_price'][0])
                #condicion de compras cercanas a 10 USD
                if (saldo * 0.25) <= 11:
                    quantity = round((11/price), decimal_quantity)
                else:
                    quantity = round((saldo*0.25) / price, decimal_quantity)
                
                #envio orden de compra
                buy_order = new_order(per, 'BUY', price, quantity)

                #variable para tomar tiempo:
                time_order = 0

                #entro en bucle esperando que la orden reciente se confirme, para generar stop loss
                while time_order < 120:
                     if client.get_order(per, orderId=str(buy_order['orderId']))['status'] == 'FILLED':
                        #registro el trader
                        traders.append(client.get_order(per, orderId=str(buy_order['orderId'])))
                        #guardo el precio para calcular el take profit
                        price_take_profit = float(buy_order['price']) * 1.02
                        #calculo para stop_loss
                        stop_price = round(price * 0.99, decimal_price)
                        saldo -= (price * quantity)
                        compras += 1
                        buy = True
                        break
                     time.sleep(2)
                     time_order += 1


        """VENDER"""
        if #estrategia de venta:    
            #consulto la cantidad de posesiones que tengo y precio actual
            quantity_pos = float(next(x for x in client_account['balances'] if x["asset"] == symbol)['free'])
            price = float(get_order_book(per)['ask_price'][0]) #ultimo precio de venta
            
            #si tengo para vender, vendo
            if ((quantity_pos * price) >= 10):
                
                quantity = round(quantity_pos - 0.1, decimal_quantity)
                
                #envio orden de compra
                sell_order = new_order(per, 'SELL', price, quantity)
                
                #variable para tomar tiempo:
                time_order = 0

                while time_order < 120:
                     if client.get_order(per, orderId=str(sell_order['orderId']))['status'] == 'FILLED':
                        #registro el trade 
                        traders.append(client.get_order(per, orderId=str(sell_order['orderId'])))
                        
                        saldo += (price * quantity)
                        ventas += 1
                        buy = False
                        #reseteo precios stops
                        stop_price = 0
                        stop_take_price = 0
                        break
                     time.sleep(2)
                     time_order += 1
                     
                     
        """VENTA STOP LOSS O TAKE PROFIT"""
        if (float(data['Close'][-2] < stop_price)) or (float(data['Close'][-2] < stop_take_price)) :
            #consulto la cantidad de posesiones que tengo y precio actual
            quantity_pos = float(next(x for x in client_account['balances'] if x["asset"] == symbol)['free'])
            price = float(get_order_book(per)['ask_price'][0]) #ultimo precio de venta

            #si tengo para vender, vendo
            if ((quantity_pos * price) >= 10):
                
                quantity = round(quantity_pos - 0.1, decimal_quantity)
                
                #envio orden de compra
                sell_order = new_order(per, 'SELL', price, quantity)
            
                #variable para tomar tiempo:
                time_order = 0
            
                while time_order < 120:
                     if client.get_order(per, orderId=str(sell_order['orderId']))['status'] == 'FILLED':
                        #registro el trade 
                        traders.append(client.get_order(per, orderId=str(sell_order['orderId'])))
                        
                        saldo += (price * quantity)
                        
                        if float(data['Close'][-2]) < stop_price: 
                            stops_loss += 1
                        else:
                            take_profit += 1 
                        buy = False
                        
                        #reseteo de stops
                        stop_price = 0
                        stop_take_price = 0     
                        break
                     time.sleep(2)
                     time_order += 1
            
            
        """ACTUALIZO TAKE PROFIT"""
        if (buy) & (float(data.Close[-2]) > price_take_profit):
            price_take_profit = float(data.Close[-2]) #actualizo price
            #nuevo stop loss
            stop_take_price = round(float(data.Close[-2]) * 0.985, decimal_price)

        """      
        if len(traders) > 0:
            traders_xlsx = pd.DataFrame(traders).set_index(['time'])
            traders_xlsx.index = pd.to_datetime(traders_xlsx.index, unit='ms')
            traders_xlsx.to_excel('Registro + ' + str(per) + '4.xlsx')
            #traders = pd.read_excel('Registro + APEUSDT.xlsx') #"index_col" indico la primer columna
        """
         
        ciclos +=1
        print(f"\n - {ciclos} ciclos \n - {compras} compras \n - {ventas} ventas \n - {stops_loss} stops loss \n - {take_profit} take profit \n - RSI: {round(data['RSI'][-1],2)} \n - Precio: {data['Close'][-1]}" )
        
        data_graf = data.loc[data.index > (dt.datetime.now() - dt.timedelta(days=2))]
        fig, axs = plt.subplots(nrows=3, figsize=(25,15), gridspec_kw={'height_ratios':[1,3,1]})
        axs[0].plot(data_graf.index, data_graf.ADX, lw=1)
        axs[0].axhline(50, lw=1, color='red', ls='--')
        axs[0].text(data_graf.index[-1], data_graf.ADX[-1], round(data_graf.ADX[-1],2), color = 'black')
        axs[1].plot(data_graf.index, data_graf.Close, lw=1)
        axs[1].text(data_graf.index[-1], data_graf.Close[-1], round(data_graf.Close[-1],2), color = 'black')
        if len(traders) > 0:
            axs[1].scatter(x=[pd.to_datetime(t['time'], unit='ms') for t in traders], y=[float(t["price"]) if t["side"] == 'BUY' else np.nan for t in traders], marker='^', color='g')
            axs[1].scatter(x=[pd.to_datetime(t['time'], unit='ms') for t in traders], y=[float(t["price"]) if t["side"] == 'SELL' else np.nan for t in traders], marker='v', color='r')
        axs[2].plot(data_graf.index, data_graf.RSI, color='black', lw=1)
        axs[2].axhline(25, lw=1, color='red', ls='--')
        axs[2].axhline(75, lw=1, color='red', ls='--')
        axs[2].text(data_graf.index[-1], data_graf.RSI[-1], round(data_graf.RSI[-1],2), color = 'black')
        plt.show()
        
        
        
