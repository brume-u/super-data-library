# super-data-library
A Python data library that allows you to download financial time series, store them in databases and use them quickly.

The Jupyter notebook data_retrieval_testing.ipynb demonstrates how to the library works.

The files mysql_arguments_example.py and vantage_data_examp;e.py should have their strings filled with personal keys in order for the library to run on your own systems.

A "mongodb_tools.py" will be added so to enable you to store and access data in a MongoDB database.
New "api_tools.py" may be added in the future so that one can pull data from other sources.

This library is intended for financial analysis and so contains sector_to_stocks and industry_to_stocks which contain JSON that save time
in generating their respective dictionaries. They are used in the main notebook, data_retrieval_testing.ipynb and will be useful in
performing the Pairs Trading analysis that I will be uploading shortly.
