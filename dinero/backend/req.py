"""
Module for retrieving news articles related to a specific stock ticker.

    Function :
    -   get_news_articles

"""
import requests

def get_news_articles(ticker : str, date: str) :
    """
    Retrieve news articles related to a specific stock ticker on a given date.

    Args:
        ticker (str): The stock ticker symbol.
        date (str): The date for which news articles are to be retrieved.
                    Should be in the format 'YYYY-MM-DD'.
    Returns:
        dict: A dictionary containing the news articles data.

    
    """
    url = f'https://eodhd.com/api/news?s={ticker}&offset=0&api_token=demo&fmt=json&from={date}&to={date}'
    data = requests.get(url, timeout= 100).json()
    return data
