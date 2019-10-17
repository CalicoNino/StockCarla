#!/usr/bin/env python

# Based off https://www.youtube.com/watch?v=zwqwlR48ztQ

from forex import *
from crypto import *
from stockTime import *

import numpy as np
import matplotlib.pyplot as py
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

global api_key, symbol
api_key = '91IGP67JSL4LZM0L'
symbol = 'AAPL'


if __name__ == '__main__':
    ST = stockTime(api_key, symbol)
    # printTuple(ST.time_intraday())
    data = ST.time_intraday()[1]
    training_set = data.iloc[:, 1:2].values
    # print(training_set)

    sc = MinMaxScaler(feature_range = (0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    # print(training_set_scaled)

    x_train = []
    y_train = []

    for i in range(60,  len(training_set_scaled)):
            x_train.append(training_set_scaled[i-60:i, 0])
            y_train.append(training_set_scaled[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    # print(x_train)

    regressor = Sequential()

    regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units = 50, return_sequences = True))
    regressor.add(Dropout(0.2))

    regressor.add(LSTM(units = 50))
    regressor.add(Dropout(0.2))

    regressor.add(Dense(units = 1))

    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

    regressor.fit(x_train, y_train, epochs = 100, batch_size = 32)

    # Getting the predicted stock price of 2017
    inputs = training_set
    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)
    X_test = []
    for i in range(60, 100):
        X_test.append(inputs[i-60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    real_stock = training_set[-20:]

    # # Visualising the results
    plt.plot(real_stock, color = 'red', label = 'Real')
    plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted')
    plt.title('Price Prediction')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
