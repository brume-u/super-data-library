import pandas as pd

from sqlalchemy import create_engine
import urllib.parse
from decouple import config

dialect = "mysql"
driver = "pymysql"
user = config('MYSQL_USER')
password = config('MYSQL_PASSWORD')
password = urllib.parse.quote_plus(password)database = "stocks"
host = config('MYSQL_HOST')
port = config('MYSQL_PORT')
address = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"
sqlEngine = create_engine(address)


def to_db(symbol, series):
    """Stores the data in the right table of our database."""
    with sqlEngine.begin() as connection:
        series.to_sql(symbol.lower(), connection, if_exists='replace')


def get_from_db(symbol, start_date, end_date):
    """Returns a time series from our database for a symbol of entries that fall within the given dates (inclusive)."""
    with sqlEngine.begin() as connection:
        series = pd.read_sql(
            "SELECT * FROM " + symbol + " WHERE date >= '" + start_date + "' AND date <= '" + end_date + "'",
            connection, index_col="date")
    return series


def data_in_db(symbol, start_date, end_date):
    """Checks if the data we are looking for is already in database, and returns it if so, otherwise returns
    some form of error.
    """
    in_db = False
    with sqlEngine.begin() as connection:
        results = connection.execute("SHOW TABLES")
        for x in results:
            proxy = "('" + symbol.lower() + "',)"  # The format of table names in results

            # Checking if there are dates that lie within the table. This does not check that data for all dates is in the table
            # but the method by which we attain this data should mean that this isn't a problem.
            if proxy == str(x) and dates_in_table(symbol, start_date, end_date, connection):
                in_db = True
    return in_db


def dates_in_table(symbol, start_date, end_date, connection):
    """Checks if we have data in symbol's table for a specific date. Returns a Boolean."""
    series = get_from_db(symbol, start_date,
                         end_date)  # There is perhaps redundancy here as we open engine in get_from_db too.
    if len(series) >= 1:
        return True
    return False