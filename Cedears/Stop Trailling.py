"""
Created on Thu Mar 18 18:01:37 2021

@author: Niko
"""
import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'ABT', 'MMM', 'MSFT', 'ORCL']
price = pd.DataFrame()
data = pd.DataFrame()
stop_trailing = pd.DataFrame()
stop = 0.95


data = yf.download(tickers, start='2021-03-22')

data = data.drop(['Close', 'Open', 'Volume', 'High', 'Low'], axis=1)

for i in tickers:
    n=0
    price[i] = data['Adj Close'][i]
    price[i, 'Shift'] = price[i].shift()
    stop_trailing[i] = price[i]*0
    while n < len(price[i]):
        if price[i][n] > price[i,'Shift'][n]:
            stop_trailing[i] = price[i][n] * stop
                
        elif price[i][n] < stop_trailing[i][n]:
            print([i], 'VENDER YA')
        n+=1 
    
print('Termino')
"""
prices_buy = [0]
prices_stops_buy = [0]
prices_sell = []
price = 0
n = 0
new_price_stop = 0.0
q = input ("BUY o SELL: ").upper()

while price != True:
    
    if q == "BUY":
        stop = 0.05
        price = float(input("Precio: "))
        stop_trailing = price * stop
        price_stop = price - stop_trailing
        prices_buy.append(price)
        prices_stops_buy.append(price_stop)
        if prices_stops_buy[n+1] > prices_stops_buy[n]:
            new_price_stop = price_stop
            print("PASO POR ACA")
        if price < new_price_stop:
            print("VENDER")
        if price > new_price_stop:
            print("MANTENER")
        n = n + 1
        

   else:
        stop = 0.05
        price = input("Precio: ")
        stop_trailing = float(price) * stop
        price_stop = float(price) + stop_trailing
        print(price_stop)
else:
    print("Finalizado")

""" 
