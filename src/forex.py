#!/usr/bin/env python

import requests
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
import numpy as np

global api_key, from_symbol, to_symbol
api_key = '91IGP67JSL4LZM0L'
from_symbol = 'EUR'
to_symbol = 'USD'


class forex():
    def __init__(self, api_key, from_symbol, to_symbol):
        self.key = api_key
        self.to_sym = to_symbol
        self.from_sym = from_symbol

    def currency_exchRate(self):
        data = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+self.from_sym+'&to_currency='+self.to_sym+'&apikey='+self.key)
        data = data.json()
   
        data = data['Realtime Currency Exchange Rate']
        df = pd.DataFrame(columns = [data.items()[6][0][3:], data.items()[0][0][3:], data.items()[4][0][3:], data.items()[2][0][3:], data.items()[3][0][3:], data.items()[5][0][3:], data.items()[1][0][3:]]) 
        df.loc[0] = [data.items()[6][1], data.items()[0][1], data.items()[4][1], data.items()[2][1], data.items()[3][1], datetime.datetime.strptime(data.items()[5][1], '%Y-%m-%d %H:%M:%S'), data.items()[1][1]]
        print(df)

    def time_intraday(self, t = 1, f = 'compact'): #1, 5, 15, 30, 60
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol='+self.from_sym+'&to_symbol='+self.to_sym+'&interval='+str(t)+'min&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[3][0][3:], meta.items()[4][0][3:], meta.items()[6][0][3:], meta.items()[0][0][3:], meta.items()[5][0][3:], meta.items()[1][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[3][1], meta.items()[4][1], meta.items()[6][1], datetime.datetime.strptime(meta.items()[0][1], '%Y-%m-%d %H:%M:%S'), meta.items()[5][1], meta.items()[1][1], meta.items()[2][1]]
    
        data = data['Time Series FX ('+str(t)+'min)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)

    def time_daily(self, f = 'compact'):
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+self.from_sym+'&to_symbol='+self.to_sym+'&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[5][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[5][1], datetime.datetime.strptime(meta.items()[3][1], '%Y-%m-%d %H:%M:%S'), meta.items()[4][1], meta.items()[2][1]]

        data = data['Time Series FX (Daily)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)
        
    def time_weekly(self):
        data = requests.get('https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol='+self.from_sym+'&to_symbol='+self.to_sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[4][1], '%Y-%m-%d %H:%M:%S'), meta.items()[2][1]]

        data = data['Time Series FX (Weekly)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)

    def time_monthly(self):
        data = requests.get('https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol='+self.from_sym+'&to_symbol='+self.to_sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[4][1], '%Y-%m-%d %H:%M:%S'), meta.items()[2][1]]

        data = data['Time Series FX (Monthly)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)

if __name__ == '__main__':
    A = forex(api_key, from_symbol, to_symbol)
    # A.currency_exchRate()
    # A.time_intraday()
    # A.time_daily()
    # A.time_weekly()
    # A.time_monthly()




