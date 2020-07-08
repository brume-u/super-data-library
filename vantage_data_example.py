"""vantage_data.py

A file containing methods for retrieving data from the Alpha Vantage API. Fill in your key for the website below.
"""


import pandas
from datetime import date
import time
from alpha_vantage.timeseries import TimeSeries


# Fill in your key here. If you do not have one, register with Alpha Vantage at https://www.alphavantage.co/
key = ""

ts = TimeSeries(key, output_format='pandas')


last_date = date.today()
requests_today = 0
requests_this_second = 0

def get_data(symbol):
    """Takes a symbol and retrieves the adjusted close data between the dates listed. This data is output as
    csv/pandas/json"""
    global key, ts, last_date, requests_today, requests_this_second
    if last_date != date.today():
        last_date = date.today()
        requests_today = 0
        requests_this_second = 0
    if requests_today >= 500:
        raise Exception("Alpha Vantage API request limit reached for today")
    if requests_this_second >= 5:
            print("Warning: Cannot perform more than 5 Alpha Vantage APR requests every 5 minutes. This may take a while.")
            time.sleep(300)
            requests_this_second = 0
    data, meta = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    requests_today += 1
    requests_this_second += 1
    series = data["5. adjusted close"]
    series.name = symbol
    return series

