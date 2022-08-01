# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:04:21 2022

@author: Niko
"""
import pandas as pd
#import requests
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import talib
#import numpy as np

"""
tickers = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOGE', 'DOT',
           'SHIB', 'WBTC', 'STETH', 'MATIC', 'CRO', 'NEAR', 'LTC', 'TRX', 'ATOM', 'LINK', 'APE3',
           'UNI1', 'FTT', 'LEO', 'XLM', 'ALGO', 'XMR', 'FIL', 'HBAR', 'MANA', 'ICP',
           'VET', 'EGLD', 'SAND', 'THETA', 'TONCOIN', 'FRAX', 'RUNE', 'FTM', 'XTZ', 'GMT3',
           'AXS', 'CAKE', 'KLAY', 'AAVE', 'EOS', 'DFI', 'ZEC', 'KCS', 'FLOW', 'HNT',
           'GRT1', 'WAVES', 'MIOTA', 'MKR', 'CVX', 'XEC', 'HT', 'STX', 'NEO']
"""
tickers = ['BTC-USD',
           'ETH-USD',
           'USDT-USD',
           'USDC-USD',
           'BNB-USD',
           'ADA-USD',
           'XRP-USD',
           'BUSD-USD',
           'SOL-USD',
           'DOGE-USD',
           'DOT-USD',
           'HEX-USD',
           'WBTC-USD',
           'WTRX-USD',
           'TRX-USD',
           'AVAX-USD',
           'DAI-USD',
           'STETH-USD',
           'SHIB-USD',
           'MATIC-USD',
           'LEO-USD',
           'CRO-USD',
           'LTC-USD',
           'YOUC-USD',
           'NEAR-USD',
           'UNI1-USD',
           'FTT-USD',
           'LINK-USD',
           'XLM-USD',
           'BCH-USD',
           'XMR-USD',
           'BTCB-USD',
           'ETC-USD',
           'ALGO-USD',
           'XCN1-USD',
           'ATOM-USD',
           'FLOW-USD',
           'VET-USD',
           'HBAR-USD',
           'MANA-USD',
           'XTZ-USD',
           'APE3-USD',
           'ICP-USD',
           'SAND-USD',
           'KCS-USD',
           'FIL-USD',
           'TONCOIN-USD',
           'WBNB-USD',
           'EGLD-USD',
           'FRAX-USD',
           'AAVE-USD',
           'ZEC-USD',
           'THETA-USD',
           'AXS-USD',
           'EOS-USD',
           'TUSD-USD',
           'HNT-USD',
           'HBTC-USD',
           'MKR-USD',
           'KLAY-USD',
           'HT-USD',
           'BTT-USD',
           'DFI-USD',
           'BSV-USD',
           'GRT1-USD',
           'BTT2-USD',
           'MIOTA-USD',
           'RUNE-USD',
           'XEC-USD',
           'USDP-USD',
           'FTM-USD',
           'WAVES-USD',
           'NEO-USD',
           'USDN-USD',
           'QNT-USD',
           'CHZ-USD',
           'CAKE-USD',
           'LRC-USD',
           'LUSD-USD',
           'STX-USD',
           'OKB-USD',
           'NEXO-USD',
           'USDD-USD',
           'ZIL-USD',
           'DASH-USD',
           'CRV-USD',
           'PAXG-USD',
           'GMT3-USD',
           'KSM-USD',
           'BAT-USD',
           'CELO-USD',
           'ENJ-USD',
           'SAFE1-USD',
           'GALA-USD',
           'KAVA-USD',
           'CVX-USD',
           'LUNA1-USD',
           'GNO-USD',
           'ONE1-USD',
           'DCR-USD',
           ]
screener = pd.DataFrame(index=([tickers]), columns=('STD', 'RSI'))

for ticker in tickers:
    data = yf.download(ticker, start=str((dt.date.today())-(dt.timedelta(days=7))), interval='5m')
    screener['STD'][ticker] = round(data['Close'].pct_change().std()*100, 4)
    data = yf.download(ticker, start=str((dt.date.today())-(dt.timedelta(days=365))))
    if (talib.RSI(data['Close'], timeperiod=14))[-1] > 0:
        screener['RSI'][ticker] = float((talib.RSI(data['Close'], timeperiod=14))[-1])

pd.to_numeric(screener['STD'])

fig, ax = plt.subplots(figsize=(35,10))
rects1 = ax.bar(tickers, screener['STD'], label='STD', ec='gray')
ax.set_ylabel('STD')
ax.set_xticklabels(screener.index, rotation=90)
ax.bar_label(rects1, padding=3)
plt.show()


"""
rsi = {}
for ticker in tickers:
    data = yf.download(ticker+'-USD', start=str((dt.date.today())-(dt.timedelta(days=365))))
    data = data.drop(['Adj Close', 'High', 'Low', 'Open', 'Volume'], axis=1)
    if (talib.RSI(data['Close'], timeperiod=14))[-1] > 0:
        rsi[ticker] = (talib.RSI(data['Close'], timeperiod=14))[-1]
"""

