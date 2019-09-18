#!/usr/bin/env python

import requests
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
import numpy as np

global api_key, from_symbol, to_symbol
api_key = '91IGP67JSL4LZM0L'
from_symbol = 'BTC'
to_symbol = 'USD'

class crypto():
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

    def time_daily(self):
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[2][0][3:], meta.items()[5][0][3:], meta.items()[1][0][3:], meta.items()[4][0][3:], meta.items()[0][0][3:], meta.items()[3][0][3:], meta.items()[6][0][3:]] )
        dmeta.loc[0] = [meta.items()[2][1], meta.items()[5][1], meta.items()[1][1], meta.items()[4][1], meta.items()[0][1], meta.items()[3][1], meta.items()[6][1]]
        
        data = data['Time Series (Digital Currency Daily)']
        df = pd.DataFrame(columns= ['Timestamp','(a)Open ('+self.to_sym+')', '(a)High ('+self.to_sym+')', '(a)Low ('+self.to_sym+')', '(a)Close ('+self.to_sym+')', 'Volume', 'Market Cap ('+self.to_sym+')', '(b)Open ('+self.to_sym+')', '(b)High ('+self.to_sym+')', '(b)Low ('+self.to_sym+')', '(b)Close ('+self.to_sym+')'] )
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1a. open ('+self.to_sym+')']), float(p['2a. high ('+self.to_sym+')']), float(p['3a. low ('+self.to_sym+')']), float(p['4a. close ('+self.to_sym+')']), float(p['5. volume']), float(p['6. market cap ('+self.to_sym+')']), float(p['1b. open ('+self.to_sym+')']), float(p['2b. high ('+self.to_sym+')']), float(p['3b. low ('+self.to_sym+')']), float(p['4b. close ('+self.to_sym+')'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)

    def time_weekly(self):
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[2][0][3:], meta.items()[5][0][3:], meta.items()[1][0][3:], meta.items()[4][0][3:], meta.items()[0][0][3:], meta.items()[3][0][3:], meta.items()[6][0][3:]] )
        dmeta.loc[0] = [meta.items()[2][1], meta.items()[5][1], meta.items()[1][1], meta.items()[4][1], meta.items()[0][1], meta.items()[3][1], meta.items()[6][1]]

        data = data['Time Series (Digital Currency Weekly)']
        df = pd.DataFrame(columns= ['Timestamp','(a)Open ('+self.to_sym+')', '(a)High ('+self.to_sym+')', '(a)Low ('+self.to_sym+')', '(a)Close ('+self.to_sym+')', 'Volume', 'Market Cap ('+self.to_sym+')', '(b)Open ('+self.to_sym+')', '(b)High ('+self.to_sym+')', '(b)Low ('+self.to_sym+')', '(b)Close ('+self.to_sym+')'] )
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1a. open ('+self.to_sym+')']), float(p['2a. high ('+self.to_sym+')']), float(p['3a. low ('+self.to_sym+')']), float(p['4a. close ('+self.to_sym+')']), float(p['5. volume']), float(p['6. market cap ('+self.to_sym+')']), float(p['1b. open ('+self.to_sym+')']), float(p['2b. high ('+self.to_sym+')']), float(p['3b. low ('+self.to_sym+')']), float(p['4b. close ('+self.to_sym+')'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)

    def time_monthly(self):
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[2][0][3:], meta.items()[5][0][3:], meta.items()[1][0][3:], meta.items()[4][0][3:], meta.items()[0][0][3:], meta.items()[3][0][3:], meta.items()[6][0][3:]] )
        dmeta.loc[0] = [meta.items()[2][1], meta.items()[5][1], meta.items()[1][1], meta.items()[4][1], meta.items()[0][1], meta.items()[3][1], meta.items()[6][1]]

        data = data['Time Series (Digital Currency Monthly)']
        df = pd.DataFrame(columns= ['Timestamp','(a)Open ('+self.to_sym+')', '(a)High ('+self.to_sym+')', '(a)Low ('+self.to_sym+')', '(a)Close ('+self.to_sym+')', 'Volume', 'Market Cap ('+self.to_sym+')', '(b)Open ('+self.to_sym+')', '(b)High ('+self.to_sym+')', '(b)Low ('+self.to_sym+')', '(b)Close ('+self.to_sym+')'] )
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1a. open ('+self.to_sym+')']), float(p['2a. high ('+self.to_sym+')']), float(p['3a. low ('+self.to_sym+')']), float(p['4a. close ('+self.to_sym+')']), float(p['5. volume']), float(p['6. market cap ('+self.to_sym+')']), float(p['1b. open ('+self.to_sym+')']), float(p['2b. high ('+self.to_sym+')']), float(p['3b. low ('+self.to_sym+')']), float(p['4b. close ('+self.to_sym+')'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)

if __name__ == '__main__':
    A = crypto(api_key, from_symbol, to_symbol)
    A.currency_exchRate()
    # A.time_daily()
    # A.time_weekly()
    # A.time_monthly()