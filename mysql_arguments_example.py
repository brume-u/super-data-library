""" mysql_arguments_git.py

A file to be filled in with the details for your mysql server and databases.
"""

import urllib.parse
username = ""
password = ""
password = urllib.parse.quote_plus(password)
host = ""
port = ""

# This is the table that you will store your daily adjusted stock price data in, mine is called "stocks" but you may call it 
# whatever you like.
database = "stocks"  