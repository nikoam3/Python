# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 11:27:56 2022

@author: Niko
"""

import pandas as pd
import datetime as dt
import talib
import matplotlib.pyplot as plt
import numpy as np
import requests

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


"VARIABLES A CONFIGURAR"
per = 'APEUSDT' #par
symbol = 'APE' #simbolo
saldo_inicial = 20 #saldo inicial
stop_loss_porc = 0.98 #porcentaje del stop
take_profit_porc = 1.01 #porcentaje del take
days = 30 #dias a testear
rsi_buy = 25
rsi_sell = 75
sar_buy = 0.97
sar_sell = 1.04


"INICIO DE VARIABLES"
saldo = saldo_inicial
decimal_price = 4 #cantidad de decimales a redondear en precios
decimal_quantity = 2 #cantidad de decimales a redondear en cantidad
buy = False #estado de bot, comprado
ciclos = 0
compras = 0
ventas = 0
ventas_stop_loss = 0
ventas_take_profit = 0
comision_total = 0
quantity_pos = 0
price_take_profit = 0
open_orders = 0
stop_price = 0
stop_take_price = 0
stop_loss_order = []
buy_order = []
sell_order = []
traders = [] #almaceno traders confirmados
data = pd.DataFrame()

"ARMADO DE DATA"
inicio = dt.datetime.now() - dt.timedelta(days=days)
fecha_fin = int(dt.datetime.now().timestamp()) * 1000
while inicio < pd.to_datetime(fecha_fin,unit='ms'):
    data_temp = prices(per, '5m', None, fecha_fin)
    fecha_fin = int((data_temp.index[0] - dt.timedelta(minutes=5)).timestamp())*1000
    data = pd.concat([data_temp,data])

"CALCULOS DE I.T."
data['ADX'] = talib.ADX(data.High, data.Low, data.Close)
#data['+DI'] = talib.PLUS_DI(data.High, data.Low,data.Close, timeperiod=14)
#data['-DI'] = talib.MINUS_DI(data.High, data.Low,data.Close, timeperiod=14)
#data['MM'] = talib.EMA(data.Close, timeperiod=200)
data['SAR'] = talib.SAR(data.High, data.Low, acceleration=0.02, maximum=0.2)
data['RSI'] = talib.RSI(data.Close, timeperiod=14)
data['Vol_Med'] = talib.MA(data.Volume, timeperiod=20)
#data = data.dropna()


for x in data.iterrows():
    #print(x[1]['Close'])
    #break
    
    "---COMPRA---"    
    #consulta de SAR y RSI para COMPRAR
    #if de estrategia de compra    
        #si mi saldo me deja, compro
        if saldo > 11:
            price = round(x[1]['Close'], decimal_price)
            if (saldo * 0.25) <= 11:
                quantity = round((11/price), decimal_quantity)
            else:
                quantity = round((saldo*0.25) / price, decimal_quantity)
            #condicion de compras cercanas a 10 USD
            #quantity = round((11/price)*0.999, decimal_quantity)

            #sumo los tokens a mi posesion
            quantity_pos += quantity
            
            #calculo comision
            comision_total += quantity * 0.001
            
            #registro el trader
            saldo -= (price * quantity)
            compras += 1
            traders.append({'Tipo': 'Compra', 'Precio': price,
                            'Cantidad': quantity, 'Saldo': saldo, 
                            'Hora': x[0], 'Posesion': quantity_pos,
                            'Comisiones': comision_total})
            
            #guardo el precio para calcular el take profit
            """
            if x[1]['Close'] < x[1]['MM']:
                take_profit_porc = 1.01
                stop_loss_porc = 0.99
            else:
                take_profit_porc = 1.02
                stop_loss_porc = 0.98
            """
            price_take_profit = round(price * take_profit_porc, decimal_price)
           
            #calculo para stop_loss
            stop_price = round(price * stop_loss_porc, decimal_price)
            
            #cargo ordenes a la lista de espera
            open_orders += 1
            
            buy = True
    
    "---VENTA---"
    #consulta de SAR y RSI para VENDER
    #if de estrategia de venta    

        price = round(x[1]['Close'], decimal_price)
        
        #si tengo para vender, vendo
        if ((quantity_pos * price) >= 10):
            
            quantity = round((quantity_pos) * 0.999, decimal_quantity)

            #resto los tokens a mi posesion(multiplico  un porcentaje para holdear)
            quantity_pos -= quantity * 0.999
            
            #calculo y suma de comision
            comision_total += quantity * 0.001
            
            #registro el trade 
            saldo += (price * quantity)
            ventas += 1
            buy = False
            traders.append({'Tipo': 'Venta', 'Precio': price,
                            'Cantidad': quantity, 'Saldo': saldo, 
                            'Hora': x[0], 'Posesion': quantity_pos,
                            'Comisiones': comision_total})
            
            open_orders -= 1
            
    "---STOP LOSS o TAKE PROFIT---"
    #analizo si algun stop se confirmo
    if (float(x[1]['Close']) < stop_price) or (float(x[1]['Close']) < stop_take_price):
        
        price = round(x[1]['Close'], decimal_price)
        
        #si tengo para vender, vendo
        if ((quantity_pos * price) >= 10):
            
            quantity = round((quantity_pos) * 0.999, decimal_quantity)

            #resto los tokens a mi posesion(multiplico  un porcentaje para holdear)
            quantity_pos -= quantity * 0.999
            
            #calculo y suma de comision
            comision_total += quantity * 0.001
            
            #registro el trade 
            saldo += (price * quantity)
            ventas += 1
            buy = False
            open_orders -= 1
            
            #registro el trader
            if (float(x[1]['Close']) < stop_price):
                ventas_stop_loss += 1
                traders.append({'Tipo': 'Stop_Loss', 'Precio': price,
                                'Cantidad': quantity, 'Saldo': saldo, 
                                'Hora': x[0], 'Posesion': quantity_pos,
                                'Comisiones': comision_total})
            else:
                ventas_take_profit += 1
                traders.append({'Tipo': 'Take_Profit', 'Precio': price,
                                'Cantidad': quantity, 'Saldo': saldo, 
                                'Hora': x[0], 'Posesion': quantity_pos,
                                'Comisiones': comision_total})
            
            #reseteo precios stops
            stop_price = 0
            stop_take_price = 0
            
            
        
    "---TAKE PROFIT---"
    #si estoy comprado, analizo mi take profit y actualizo el stop loss
    if (buy) & ((float(x[1]['Close'])) > price_take_profit):
        price_take_profit = float(x[1]['Close'])  #actualizo price
        
        #nuevo stop loss
        """
        if x[1]['Close'] < x[1]['MM']:
            stop_take_price = float(x[1]['Close']) * 0.99
        else:
            stop_take_price = float(x[1]['Close']) * 0.98
        """
        stop_take_price = float(x[1]['Close']) * 0.98
               
                   
    ciclos +=1

traders = pd.DataFrame(traders).set_index(["Hora"])
print(f"\n Rendimiento Precio {((traders.Precio[-1]/traders.Precio[-0])-1)*100} \n Rendimiento Saldo {((((quantity_pos*data.Close[-1]) + saldo)/saldo_inicial)-1)*100} ")
print(f"\n - {ciclos} ciclos \n - {compras} compras \n - {ventas} ventas \n - {ventas_stop_loss} stop_loss \n - {ventas_take_profit} take_profit" )

"GRAFICAR"
#filtro periodo de traders
data = data.loc[(data.index >= traders.index[0]) & (data.index <= traders.index[-1])]
fig, axs = plt.subplots(nrows=3, figsize=(25,15), gridspec_kw={'height_ratios':[1,3,1]})

axs[0].plot(data.index, data.ADX, lw=1, color='black')
axs[0].axhline(50, lw=1, color='red', ls='--')
axs[1].scatter(x=traders.index, y=[i[1].Precio if i[1].Tipo == 'Compra' else np.nan for i in traders.iterrows()], marker='^', color='g')
axs[1].scatter(x=traders.index, y=[i[1].Precio if i[1].Tipo == 'Venta' or i[1].Tipo == 'Stop_Loss'  else np.nan for i in traders.iterrows()], marker='v', color='r')
axs[1].scatter(x=traders.index, y=[i[1].Precio if i[1].Tipo == 'Take_Profit' else np.nan for i in traders.iterrows()], marker='v', color='b')
axs[1].plot(data.index, data.Close, lw=1)
axs[2].plot(data.index, data.RSI, color='black', lw=1)
axs[2].axhline(25, lw=1, color='red', ls='--')
axs[2].axhline(75, lw=1, color='red', ls='--')
plt.show()




