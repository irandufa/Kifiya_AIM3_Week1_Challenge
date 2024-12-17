import yfinance as yf
import talib as ta
import pandas as pd
import numpy as np
import plotly.express as px
from pypfopt.efficient_frontier import EfficientFrontier

from pypfopt import risk_models
from pypfopt import expected_returns

class FinancialAnalyzer:
    def __init__(self, ticker, start_date, end_date):
        self.ticker=ticker
        self.start_date=start_date
        self.end_date=end_date
    def retrieve_stockdata(self):
        return yf.download(tickers="AAPL", start=self.start_date, end=self.end_date)
    def calculate_moving_avg(self, data, window_size):
        return ta.SMA(data, timeperiod=window_size)
    def calculate_technical_indicator(self, data):
        data["SMA"]=self.calculate_moving_avg(data["Close"], 20)
        data["RSI"]=ta.RSI(data["Close"], timeperiod=14)
        data["EMA"]=ta.EMA(data["Close"], timeperiod=20)
        macd, macd_signal, _=ta.MACD(data["Close"])
        data["MACD"]=macd
        data["MACD"]=macd_signal
        return data
    def plot_stock_dataset(self, data):
        fig=px.line(data, x=data.index, y=["Close", "SMA"], title="Stock price with moving avg")
        fig.show()
    def plot_rsi(self, data):
        fig=px.line(data, x=data.index, y="RSI", title="Relative Strength Index")
        fig.show()
    def plot_ema(self, data):
        fig=px.line(data, x=data.index, y=["Close", "EMA"], title="EMA")
        fig.show()
    def calculate_portifolio(self, ticker, start_date, end_date):
        data=yf.download(tickers, start_date, end_date)["Close"]
        mu=expected_returns.mean_historical_return(data)
        cov=risk_models.sample_cov(data)
        ef=EfficientFrontrier(mu, cov)
        weight=ef.max_sharpe()
        weight=dict(sip(ticker, weight.values()))
        return weight
    
