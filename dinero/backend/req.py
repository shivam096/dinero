"""
Module for retrieving news articles related to a specific stock ticker.

    Function :
    -   get_news_articles

"""
import requests

def get_news_articles(ticker: str, date: str):
    """
    Retrieve news articles related to a specific stock ticker on a given date.

    Args:
        ticker (str): The stock ticker symbol.
        date (str): The date for which news articles are to be retrieved.
                    Should be in the format 'YYYY-MM-DD'.
    Returns:
        dict: A dictionary containing the news articles data.
    """
    try:
        url = f'https://eodhd.com/api/news?s={ticker}\
            &offset=0&api_token=demo&fmt=json&from={date}&to={date}'
        response = requests.get(url, timeout=100)
        response.raise_for_status()  # Raise an exception for HTTP errors (status codes >= 400)
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error retrieving news articles: {e}")
        return None
    