from bs4 import BeautifulSoup
import requests


def get_sp500():
    """Returns up-to-date list of S&P500 symbols, scraped Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    
    attributes = []  # To store the list of symbols
    count = 0
    for span in soup.find_all('a', attrs={'class': 'external text', 'rel': 'nofollow'}):
        
        # The even indices contain the relevant information
        if count % 2 == 0:
            try:
                attributes.append(span.text)
            except:
                print('S&P500 scraping method is failing.')
        count += 1
    return attributes


sp500 = get_sp500()[:505]
sp500_short = sp500[:5]

assert sp500[0] == 'MMM' and sp500[1] == 'ABT', print("Look at S&P500 list. Something may be wrong.")


def industry_and_sector(symbol):
    """Takes a stock symbol and scrapes the Industry and Sector of that stock from Yahoo Finance. 
    """
    profile_url = 'https://uk.finance.yahoo.com/quote/' + symbol + '/profile?p=' + symbol
    request = requests.get(profile_url)
    soup = BeautifulSoup(request.content, 'lxml')
    
    attributes = []
    
    for span in soup.find_all('span', attrs={'class': 'Fw(600)'}):
        try:
            attributes.append(span.text)
        except:
            print("Industry and Sector scraping is failing.")
    sector = attributes[0]
    industry = attributes[1]
    return sector, industry  # The third element of this list is number of Full-time Employees but we don't need this


assert (industry_and_sector("MSFT")) == ('Technology', 'Software—Infrastructure'), print("Sector and Industry \
    retrieval failed. Yahoo Finance may have changed their layout.")


def generate_industry_sector_YF(symbols):
    """Returns industry to stocks and sector to stocks dictionaries from data scraped from Yahoo Finance."""
    # Todo This method is slow and the data would be better scraped when generating the sp500 list from Wikipedia 
    
    industry_to_stocks = {}
    sector_to_stocks = {}
    
    for symbol in symbols:
        sector, industry = industry_and_sector(symbol)
        
        # If the sector/industry is already a dictionary key, we append the symbol to the list. Otherwise, we create a
        # new key with a list containing only the symbol.
        if sector in sector_to_stocks.keys():
            sector_to_stocks[sector].append(symbol)
        else:
            sector_to_stocks[sector] = [symbol]
            
        if industry in industry_to_stocks.keys():
            industry_to_stocks[industry].append(symbol)
        else:
            industry_to_stocks[industry] = [symbol]
    return sector_to_stocks, industry_to_stocks