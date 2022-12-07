import datetime as dt
import pandas_datareader as web

t1 = dt.datetime.utcnow() - dt.timedelta(hours=24)
start = t1.date()
t2 = dt.datetime.utcnow()
end = t2.date()
marketInfo = web.DataReader('BTC' + '-' + 'USD', 'yahoo', start=start, end=end)
marketOpen, marketNow = marketInfo['Open'][1], marketInfo['Adj Close'][1]
priceDelta = (marketNow / marketOpen - 1) * 100
print(marketInfo)