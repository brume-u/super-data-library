import pandas as pd
from alpha_vantage.timeseries import TimeSeries


# Fill in your key here. If you do not have one, register with Alpha Vantage at https://www.alphavantage.co/
key = ""

ts = TimeSeries(key, output_format='pandas')

def get_data(symbol):
    """Takes a symbol and retrieves the adjusted close data between the dates listed. This data is output as
    csv/pandas/json"""
    global key
    global ts
    data, meta = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    series = data["5. adjusted close"]
    series.name = symbol
    return series

