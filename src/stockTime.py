#!/usr/bin/env python

import requests
import pandas as pd
import datetime 
import matplotlib.pyplot as plt
import numpy as np

global api_key, symbol
api_key = '91IGP67JSL4LZM0L'
symbol = 'AAPL'

def search_endpoint(api_key, keywords = ""):
    data = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+keywords+'&apikey='+api_key)
    data = data.json(); data = data['bestMatches']
    search = pd.DataFrame(columns = ['Symbol', 'Name', 'Type', 'Region', 'Market Open', 'Market CLose', 'Time Zone', 'Currency', 'Match Score'])
    for p in data:
        search.loc[-1,:] = [str(p['1. symbol']), str(p['2. name']), str(p['3. type']), str(p['4. region']), datetime.datetime.strptime(p['5. marketOpen'],'%H:%M'), datetime.datetime.strptime(p['6. marketClose'],'%H:%M'), 
                            str(p['7. timezone']), str(p['8. currency']), float(p['9. matchScore']) ]
        search.index = search.index + 1
    print(search)

class stockTime():
    def __init__(self, api_key, symbol):
        self.key = api_key
        self.sym = symbol

    def time_intraday(self, t = 1, f = 'compact'): #1, 5, 15, 30, 60
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.sym+'&interval='+str(t)+'min&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json()
        
        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[5][0][3:], meta.items()[2][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:], meta.items()[1][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[5][1], meta.items()[2][1], meta.items()[3][1], meta.items()[4][1], datetime.datetime.strptime(meta.items()[1][1], '%Y-%m-%d %H:%M:%S')]


        data = data['Time Series ('+str(t)+'min)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['5. volume'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)


        # data = df.sort_values('Timestamp')
        # data['Close'] = data['Close'].astype(float)
        # data['Timestamp'] = data['Timestamp']
        # data['5min'] = np.round(data['Close'].rolling(window=5).mean(),2)
        # data['5min'].plot()
        # plt.show()
        # print data
        # print data['Close']
        # print data['Timestamp']

    def time_daily(self, f = 'compact'): 
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+self.sym+'&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[2][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[2][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[4][1], '%Y-%m-%d %H:%M:%S')]

        data = data['Time Series (Daily)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['5. volume'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
        
        print(dmeta)
        print(df)

    def time_daily_adjusted(self, f = 'compact'):
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+self.sym+'&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json()

        meta = data[str(data.items()[0][0])]
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[2][0][3:], meta.items()[3][0][3:], meta.items()[4][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[2][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[4][1], '%Y-%m-%d %H:%M:%S')]

        data = data['Time Series (Daily)']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adjusted Close', 'Split Coefficient', 'Dividend Amount'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['6. volume']), float(p['5. adjusted close']), float(p['8. split coefficient']), float(p['7. dividend amount'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)

    def time_weekly(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+self.sym+'&apikey='+self.key)
        data = data.json()
        
        meta = data[str(data.items()[0][0])]
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[2][1], '%Y-%m-%d %H:%M:%S')]

        data = data['Weekly Time Series']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['5. volume'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)

    def time_weekly_adjusted(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol='+self.sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[2][1], '%Y-%m-%d %H:%M:%S')]
        
        data = data['Weekly Adjusted Time Series']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adjusted Close', 'Dividend Amount'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['6. volume']), float(p['5. adjusted close']), float(p['7. dividend amount'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
                
        print(dmeta)
        print(df)

    def time_monthly(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+self.sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[2][1], '%Y-%m-%d %H:%M:%S')]

        data = data['Monthly Time Series']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['5. volume'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        print(dmeta)
        print(df)

    def time_monthly_adjusted(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol='+self.sym+'&apikey='+self.key)
        data = data.json()

        meta = data['Meta Data']
        dmeta = pd.DataFrame(columns = [meta.items()[0][0][3:], meta.items()[1][0][3:], meta.items()[3][0][3:], meta.items()[2][0][3:]])    
        dmeta.loc[0] = [meta.items()[0][1], meta.items()[1][1], meta.items()[3][1], datetime.datetime.strptime(meta.items()[2][1], '%Y-%m-%d %H:%M:%S')]

        data = data['Monthly Adjusted Time Series']
        df = pd.DataFrame(columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adjusted Close', 'Dividend Amount'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d, '%Y-%m-%d').date()
            data_row = [date, float(p['1. open']), float(p['2. high']), float(p['3. low']), float(p['4. close']), int(p['6. volume']), float(p['5. adjusted close']), float(p['7. dividend amount'])]
            df.loc[-1,:] = data_row
            df.index = df.index + 1
                
        print(dmeta)
        print(df)

    def quote_endpoint(self):
        data = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+self.sym+'&apikey='+self.key)
        data = data.json()

        data = data['Global Quote']
        gquote = pd.DataFrame(columns = [data.items()[7][0][4:], data.items()[0][0][4:], data.items()[1][0][4:], data.items()[2][0][4:], data.items()[4][0][4:], 
                                        data.items()[8][0][4:], data.items()[5][0][4:], data.items()[3][0][4:], data.items()[6][0][4:]])    
        gquote.loc[0] = [data.items()[7][1], data.items()[0][1], data.items()[1][1][4:], data.items()[2][1], datetime.datetime.strptime(data.items()[4][1], '%Y-%m-%d'), 
                        data.items()[8][1], data.items()[5][1], data.items()[3][1], data.items()[6][1]] 
                                        
        print(gquote)

    
if __name__ == '__main__':
    # search_endpoint(api_key, 'apple')
    A = stockTime(api_key, symbol)
    # A.time_intraday()
    # A.time_daily()
    # A.time_daily_adjusted()
    # A.time_weekly()
    # A.time_weekly_adjusted()
    # A.time_monthly()
    # A.time_monthly_adjusted()
    # A.quote_endpoint()

    






