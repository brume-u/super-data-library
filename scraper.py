from bs4 import BeautifulSoup
import requests
from collections import defaultdict

def get_sp500():
    """Returns up-to-date list of S&P500 symbols, scraped from Wikipedia, and a dictionary of those stocks to the date 
    they joined the index.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')
    
    symbols = []  # To store the list of symbols
    symbol_to_date_joined = {}
    industry_to_stocks = defaultdict(list)
    sector_to_stocks = defaultdict(list)
    
    
    symbol_index = -1
    sector_index = -1
    industry_index = -1
    date_index = -1
    count_1 = 0

    for span in soup.find_all('th'):
        if span.text.strip() == "Symbol":
            symbol_index = count_1
        elif span.text == "GICS Sector":
            sector_index = count_1
        elif span.text == "GICS Sub Industry":
            industry_index = count_1
        elif span.text == "Date first added":
            date_index = count_1
        count_1 += 1
    # print(symbol_index, sector_index, industry_index, date_index)
    
    soup = BeautifulSoup(request.content, 'lxml')
    count_2 = 0
    for span in soup.find_all('td'):
        # Finding the relevant details of each symbol
        if count_2 % 9 == symbol_index:
            try:
                text = span.text.strip('\n')
                symbols.append(text)
            except Exception as e:
                print('S&P500 symbol scraping method is failing: ', e)
        elif count_2 % 9 == date_index:
            try:
                text = span.text.strip('\n')
                symbol_to_date_joined[symbols[-1]] = text
            except Exception as e:
                print('S&P500 date scraping method is failing: ', e)   
        elif count_2 % 9 == sector_index:
            sector = span.text
            sector_to_stocks[sector].append(symbols[-1])
        elif count_2 % 9 == industry_index:    
            industry = span.text
            industry_to_stocks[industry].append(symbols[-1])
        if len(symbols) >= 505:
            return symbols, symbol_to_date_joined, sector_to_stocks, industry_to_stocks
        count_2 += 1
    print("Ending late")
    return symbols, symbol_to_date_joined, sector_to_stocks, industry_to_stocks


sp500, symbol_to_date_joined, sector_to_stocks, industry_to_stocks = get_sp500()
sp500_short = sp500[:5]

assert sp500[0] == 'MMM' and sp500[1] == 'ABT', print("Look at S&P500 list. Something may be wrong. SP500 short:", sp500_short)


def industry_and_sector_YF(symbol):
    """Takes a stock symbol and scrapes the Industry and Sector of that stock from Yahoo Finance. 
    """
    symbol = symbol.replace('.', '-')
    profile_url = 'https://uk.finance.yahoo.com/quote/' + symbol + '/profile?p=' + symbol
    request = requests.get(profile_url)
    soup = BeautifulSoup(request.content, 'lxml')
    
    attributes = []
    
    for span in soup.find_all('span', attrs={'class': 'Fw(600)'}):
        try:
#             print(span.text)
            attributes.append(span.text)
        except:
            print("Industry and Sector scraping is failing.")
    try:
        sector = attributes[0]
        industry = attributes[1]
    except Exception as e:
        print(e)
        print(symbol)
        print(attributes)
        sector = "unknown"
        industry = "unknown"
    return sector, industry  # The third element of this list is number of Full-time Employees but we don't need this


assert (industry_and_sector_YF("MSFT")) == ('Technology', 'Software—Infrastructure'), print("Sector and Industry \
    retrieval failed. Yahoo Finance may have changed their layout.")


def generate_industry_sector_YF(symbols):
    """Returns industry to stocks and sector to stocks dictionaries from data scraped from Yahoo Finance."""
    # Todo This method is slow and the data would be better scraped when generating the sp500 list from Wikipedia 
    
    industry_to_stocks = {}
    sector_to_stocks = {}
    
    for symbol in symbols:
        sector, industry = industry_and_sector_YF(symbol)
        
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

### OUTDATED FUNCTIONS ###

# def get_sp500_1():
#     """Returns up-to-date list of S&P500 symbols, scraped Wikipedia."""
#     url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
#     request = requests.get(url)
#     soup = BeautifulSoup(request.content, 'lxml')
    
#     attributes = []  # To store the list of symbols
#     count = 0
#     for span in soup.find_all('a', attrs={'class': 'external text', 'rel': 'nofollow'}):
        
#         # The even indices contain the relevant information
#         if count % 2 == 0:
#             try:
#                 attributes.append(span.text)
#             except:
#                 print('S&P500 scraping method is failing.')
#         count += 1
#     return attributes

# def get_sp500_2():
#     """Returns up-to-date list of S&P500 symbols, scraped Wikipedia."""
#     url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
#     request = requests.get(url)
#     soup = BeautifulSoup(request.content, 'lxml')
    
#     attributes = []  # To store the list of symbols
#     count = 0
#     symbol_and_date = []
    
#     for span in soup.find_all('td'):
# #         print(count)
# #         print(span.text)
# #         The even indices contain the relevant information
#         if count % 9 == 0:
#             try:
#                 text = span.text.strip('\n')
#                 print("symbol", count, text)
#                 symbol_and_date.append(text)
#             except Exception as e:
#                 print('S&P500 symbol scraping method is failing: ', e)
#         elif count % 9 == 6:
#             try:
#                 text = span.text.strip('\n')
#                 print("date", count, text)
#                 symbol_and_date.append(text)
#             except Exception as e:
#                 print('S&P500 date scraping method is failing: ', e)
#             attributes.append(tuple(symbol_and_date))
#             symbol_and_date = []
#         count += 1
#     return attributes
