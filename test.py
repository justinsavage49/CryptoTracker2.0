import pandas_datareader as web
import datetime as dt

from forex_python.converter import CurrencyRates as c

t1 = dt.datetime.utcnow()
t1 = t1.date()
c.get_rate('USD', 'INR')

price = 20


print(price)