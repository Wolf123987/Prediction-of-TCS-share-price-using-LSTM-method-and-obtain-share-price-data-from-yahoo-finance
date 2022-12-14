# -*- coding: utf-8 -*-
"""To get live shares price of TCS and predict its closing price by LSTM .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-zfuqHyAlnem7H508hQKO-iHs9RHc-HA
"""

# Commented out IPython magic to ensure Python compatibility.
# %%html
# <marquee style='width: 60%;color: red;'><b>To get latest stock price  using python </b></marquee>

pip install yfinance

import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta
today = date.today()

"""To obatail current price of TCS : we took its symbol ***TCS.NS*** means NSE data of TCS 

"""

d1 = today.strftime("%Y-%m-%d")
end_date = d1
d2 = date.today() - timedelta(days=100)
d2 = d2.strftime("%Y-%m-%d")
start_date = d2

manoj = yf.download('TCS.NS', 
                      start=start_date, 
                      end=end_date, 
                      progress=False)
print(manoj.tail(50))

manoj["Date"] = manoj.index
manoj = manoj[["Date", "Open", "High", 
             "Low", "Close", "Adj Close", "Volume"]]
manoj.reset_index(drop=True, inplace=True)
print(manoj.head())

"""**plot of Date Vs Closing price of stock**"""

import plotly.express as px
import plotly.graph_objects as go
figure = px.scatter(data_frame = manoj, x="Date",
                    y="Close" ,trendline="ols")
figure.show()



"""***plot of date Vs hight price of stock ***"""

import plotly.express as px
import plotly.graph_objects as go
figure = px.scatter(data_frame = manoj, x="Date",
                    y="High" ,trendline="ols")
figure.show()

"""here is the link to get  symbols of some important stocks of national stock exchange from yahooo finance website  just repale the stock symbol like here in this program i  have taken TCS stock 
https://finance.yahoo.com/quote/%5ENSEI/components/

***Lets see the candlestick chart of TCS stock ***
"""

import plotly.graph_objects as go
figure = go.Figure(data=[go.Candlestick(x=manoj["Date"],
                                        open=manoj["Open"], 
                                        high=manoj["High"],
                                        low=manoj["Low"], 
                                        close=manoj["Close"])])
figure.update_layout(title = "TCS  Stock Price Analysis", 
                     xaxis_rangeslider_visible=False)
figure.show()

correlation = manoj.corr()
print(correlation["Close"].sort_values(ascending=False))

"""Lets try to predict the closing price of TCS by LSTM( long short-term  memory)"""

x = manoj[["Open", "High", "Low", "Volume"]]
y = manoj["Close"]
x = x.to_numpy()
y = y.to_numpy()
y = y.reshape(-1, 1)

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

"""neural network architecture for LSTM"""

from keras.models import Sequential
from keras.layers import Dense, LSTM

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape= (xtrain.shape[1], 1)))
model.add(LSTM(64, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xtrain, ytrain, batch_size=1, epochs=30)

import numpy as np
#features = [Open, High, Low, Adj Close, Volume]
features = np.array([[3100.0896, 3190.4198, 3095.0707,3120.04578, 3834845]])
model.predict(features)

"""# The ***predicted closing price of TCs is 3151.6848*** for a opening price of 3100.0896, day high of 3190.4198,day low of 3095.0707, previous day close of 3120.04578 and traded vloume of 3834845 shares """