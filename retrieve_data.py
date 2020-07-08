import pandas as pd
from datetime import datetime

import vantage_data  # Todo: Use conditional imports instead of just importing everything
import mysql_tools

APIs = {"vantage": vantage_data}
DBs = {"mysql": mysql_tools}

class PricePipeline:
    def __init__(self, api_tools="vantage", db_tools="mysql"):
        self.api_tools = APIs[api_tools]
        self.db_tools = DBs[db_tools]

    def get_pricing(self, symbols, start_date='2013-01-03', end_date='2014-01-03', symbol_reference_date=None, 
                    frequency='daily', fields=None, handle_missing='raise', start_offset=0):
        """Return the pricing data for a symbol or list of symbols given specific parameters as a Dataframe or Series.
        Designed to emulate Quantopian get.pricing() method so that the code may be transferred.
        """
        # Handling the cases where symbol is a single string or a list of strings.
        if isinstance(symbols, str):
            symbol = symbols  # Name change for clarity, maybe remove
            series = self.store_and_retrieve(symbol, start_date, end_date)
            return series
        else:
            df = pd.DataFrame([])
            for symbol in symbols:
                x = 1
                df = pd.concat([df, self.store_and_retrieve(symbol, start_date, end_date)], axis=1)
        return df


    def store_and_retrieve(self, symbol, start_date, end_date):
        """Checks if the data series is already stored in database and returns it. If not in db, downloads, stores, and
        returns it.
        """
        if self.db_tools.data_in_db(symbol, start_date, end_date):
            print("From db: " + symbol)
            series = self.db_tools.get_from_db(symbol.lower(), start_date, end_date)
            series.name = symbol.upper()
            return series
        else:
            print("Downloading: " + symbol)
            series = self.api_tools.get_data(symbol)
            self.db_tools.to_db(symbol, series)

            # Create mask to make sure that we are only returning data within the specified dates. This is done automatical in the 
            # db_tools.get_from_db() method but not in api_tools.get_data().
            mask = create_mask(series, start_date, end_date)
        return series.loc[mask]


def create_mask(series, start_date, end_date):
    """"Returns a data frame from the input series of booleans according to whether the date indices fall between
    the start_date and the end_date.
    """
    return (series.index >= datetime.strptime(start_date,"%Y-%m-%d")) & \
           (series.index <= datetime.strptime(end_date, "%Y-%m-%d"))

basic_pipeline = PricePipeline()

