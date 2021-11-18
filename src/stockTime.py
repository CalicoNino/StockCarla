#!/usr/bin/env python

import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
import ast

global api_key, symbol
api_key = '91IGP67JSL4LZM0L'
symbol = 'AAPL'

def search_endpoint(api_key, keywords = ""):
    data = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+keywords+'&apikey='+api_key)
    data = data.json(); data = data['bestMatches']
    titles = data[0].keys(); titles.sort()
    search = pd.DataFrame(columns = [i[3:].title() for i in titles])

    for result in data:
        search.loc[-1,:] = [float(result[i]) if "Score" in i else datetime.datetime.strptime(result[i],'%H:%M').time() if "market" in i else result[i] for i in titles]
        search.index = search.index + 1

    search = search.iloc[::-1]

    return search

class stockTime():
    def __init__(self, api_key, symbol):
        self.key = api_key
        self.sym = symbol

    def time_intraday(self, t = 1, f = 'compact'): #1, 5, 15, 30, 60
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.sym+'&interval='+str(t)+'min&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series ('+str(t)+'min)']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)


        # df.plot(kind ='line', x = 'Timestamp', y = 'open', color = 'red')
        # plt.show()


    def time_daily(self, f = 'compact'):
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+self.sym+'&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series (Daily)']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

    def time_daily_adjusted(self, f = 'compact'):
        if f != 'compact': f = 'full'
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+self.sym+'&outputsize='+str(f)+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series (Daily)']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

    def time_weekly(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+self.sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Weekly Time Series']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

    def time_weekly_adjusted(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol='+self.sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Weekly Adjusted Time Series']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

    def time_monthly(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+self.sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Monthly Time Series']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

    def time_monthly_adjusted(self):
        data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol='+self.sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Monthly Adjusted Time Series']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        pdf = df.iloc[::-1]

        return (dmeta, df)

    def quote_endpoint(self):
        data = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+self.sym+'&apikey='+self.key)
        data = data.json(); data = data['Global Quote'];
        titles = data.keys(); titles.sort()
        quote = pd.DataFrame(columns = [i[4:].title() for i in titles])
        quote.loc[0] = [data[i] if "symbol" in i or "percent" in i else datetime.datetime.strptime(data[i], '%Y-%m-%d').date() if "day" in i else float(data[i]) for i in titles]

        return quote

def printTuple(tuple):
    for element in tuple:
        print(element)

if __name__ == '__main__':
    # print search_endpoint(api_key, 'AAPL')
    # A = stockTime(api_key, symbol)
    # printTuple(A.time_intraday())
    # printTuple(A.time_daily())
    # printTuple(A.time_daily_adjusted())
    # printTuple(A.time_weekly())
    # printTuple(A.time_weekly_adjusted())
    # printTuple(A.time_monthly())
    # printTuple(A.time_monthly_adjusted())
    # print A.quote_endpoint()
    
    data = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+keywords+'&apikey='+api_key)

