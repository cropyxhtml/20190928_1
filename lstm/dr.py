import pandas_datareader as web
import datetime
start = datetime.datetime(2016,2,19)
end = datetime.datetime(2016,3,4)
# print(start,'&',end)
# gs = web.DataReader('078930.KS','yahoo',start,end)
# print(gs)

# gs = web.DataReader('005930.KS','yahoo','2019-09-01','2019-09-28')
# print(gs)

from pandas_datareader import data
import yfinance as yf

yf.pdr_override()

start_date = '2006-05-06'
tickers = ['067160.KQ', '035420.KS', '005930.KS']
a = [''] * len(tickers)
for i in range(len(tickers)):
    a[i] = data.get_data_yahoo(tickers[i], start_date, '2019-01-01')
for i in a:
    mcd_candle = go.Candlestick(x=i.index, open=i.Open, high=i.High, low=i.Low, close=i.Close)
    data = [mcd_candle]
    py_offline.iplot(data, filename='Candle Stick')
