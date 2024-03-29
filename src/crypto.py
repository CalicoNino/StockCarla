#!/usr/bin/env python

import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
import ast

global from_symbol, to_symbol
from_symbol = 'BTC'
to_symbol = 'EUR'

class crypto():
    def __init__(self, api_key, from_symbol, to_symbol):
        self.key = api_key
        self.to_sym = to_symbol
        self.from_sym = from_symbol

    def currency_exchRate(self):
        data = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+self.from_sym+'&to_currency='+self.to_sym+'&apikey='+self.key)
        data = data.json(); data = ast.literal_eval(json.dumps(data['Realtime Currency Exchange Rate']))
        titles = sorted(data[0].keys())

        df = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        df.loc[0] = [float(data[i]) if "Price" in i or "Rate" in i else datetime.datetime.strptime(data[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else data[i] for i in titles]

        return df

    def time_daily(self):
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = sorted(meta.keys())

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series (Digital Currency Daily)']))
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
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series (Digital Currency Weekly)']))
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
        data = requests.get('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol='+self.from_sym+'&market='+self.to_sym+'&apikey='+self.key)
        data = data.json(); meta = ast.literal_eval(json.dumps(data['Meta Data']))
        titles = meta.keys(); titles.sort()

        dmeta = pd.DataFrame(columns = [i[3:].replace("_", " ") for i in titles])
        dmeta.loc[0] = [datetime.datetime.strptime(meta[i], '%Y-%m-%d %H:%M:%S') if "Last Refreshed" in i else meta[i] for i in titles]

        data = ast.literal_eval(json.dumps(data['Time Series (Digital Currency Monthly)']))
        timestamp = data.keys(); timestamp.sort(reverse = True)
        titles = data[timestamp[0]].keys(); titles.sort()

        df = pd.DataFrame(columns= ['Timestamp'] + [i[4:] if "a." in i or "b." in i else i[3:] for i in titles])
        for date in timestamp:
            data_row = [datetime.datetime.strptime(date, '%Y-%m-%d').date()] + [float(data[date][i]) for i in titles]
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        df = df.iloc[::-1]

        return (dmeta, df)

def printTuple(tuple):
    for element in tuple:
        print(element)

# if __name__ == '__main__':
#     A = crypto(api_key, from_symbol, to_symbol)
#     print(A.currency_exchRate())
#     printTuple(A.time_daily())
#     printTuple(A.time_weekly())
#     printTuple(A.time_monthly())
