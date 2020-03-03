import urllib.parse
username = ""
password = ""
password = urllib.parse.quote_plus(password)
host = ""
port = ""

# This is the table that you will store your daily adjusted stock price data in, mine is called "stocks" but you may call it 
# whatever you like.
database = "stocks"  