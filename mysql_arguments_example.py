""" mysql_arguments_example.py

A file to be filled in with the details for your mysql server and databases. Rename to mysql_arguments.py to use with
the librar.
"""

import urllib.parse
username = ""
password = ""
password = urllib.parse.quote_plus(password)
host = ""
port = ""

# This is the database that you will store your daily adjusted stock price data in, mine is called "stocks" but you may
# call it whatever you like.
database = "stocks"  